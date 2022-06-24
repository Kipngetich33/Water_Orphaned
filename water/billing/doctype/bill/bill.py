# -*- coding: utf-8 -*-
# Copyright (c) 2021, Upande LTD. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

#std lib imports
import datetime

#application imports
from erpnext.accounts.utils import get_balance_on
from notification.sms.custom_methods.send_sms import SMSClass
from ....custom_methods.reusable_methods import get_erpnext_customer_from_customer_account,\
	get_settings

class Bill(Document):
	def before_save(self):
		self.custom_main()
		#save corresponding sales invoice
		self.create_sales_invoice()
		#send notification
		self.send_bill_notification()

	def custom_main(self):
		if self.customer_account and len(self.bill_item_details) > 0:
			pass
		else:
			frappe.throw("Customer Account and Bill Items Table cannot be empty")

		#now check if an erpnext customer account has been added
		if not self.customer:
			customer_details = get_erpnext_customer_from_customer_account(self.customer_account)
			if customer_details['status']:
				self.customer = customer_details['customer']
			else:
				frappe.throw('No Customer is linked to this Account')

		total_amount = 0 #initialize amount as 0
		#get the total amount
		for item in self.bill_item_details:
			if item.bill_item == "Other":
				#check that item price is given
				if not item.price:
					frappe.throw("Please specify item type for {}".format(item.bill_item))
			else:
				item.price = frappe.get_value('Bill Item', item.bill_item, "amount")
			#calculate totals
			item.total = item.price*item.quantity
			total_amount += item.total

		#now set the totla bill value
		self.total_bill = total_amount

	def create_sales_invoice(self):
		'''
		This is a function that creates as sales invoice
		a bill
		'''
		#check if sales bill is already linked to a sales invoice
		if self.linked_sales_invoice:
			return 
		#if its not yet linked create new invoice
		invoice_doc = frappe.new_doc("Sales Invoice")
		invoice_doc.customer  = self.customer
		#due-date
		today_date = datetime.datetime.now()
		invoice_doc.due_date  = today_date
		#loop through bill items
		for bill_item in self.bill_item_details:
			#add invoice items
			row = invoice_doc.append("items", {})
			row.item_code = bill_item.bill_item
			row.qty = bill_item.quantity
		#attempt to allocate advance payments
		invoice_doc.allocate_advances_automatically  = 1
		#now save the invoice
		invoice_doc.save(ignore_permissions = True)
		#now submite the invoice
		invoice_doc.submit()
		frappe.db.commit()
		#now link the sales invoice to the bill
		self.linked_sales_invoice = invoice_doc.name

	def send_bill_notification(self):
		'''
		Function that sends a bill notification to the
		customer
		'''
		# if already sent return
		if self.notification_sent:
			return

		#get mobile money settings
		mobile_money_settings = get_settings("Mobile Payment Settings")

		#get account details
		outstading_balance = 0
		account_balance = 0
		party_balance = get_balance_on(None,None,'Customer',self.customer,None)
		if party_balance > 0:
			outstading_balance = party_balance
		elif party_balance < 0:
			account_balance = abs(party_balance)
 
		#generate message
		message = "Dear customer you have a new bill of {}.Your outstanding balance \
			is {} and your account balance is {}.".format(self.total_bill,outstading_balance,\
			account_balance)
		#check if user has outstading balance
		if outstading_balance > 0:
			message += "Please make a payment of {} through {}:{} to continue enjoying this \
				service.".format(outstading_balance,mobile_money_settings.transaction_type,\
				mobile_money_settings.mpesa_shortcode)
		else:
			message += "Your current bill has therefore been cleared by previous payment.Thanks for\
				being a valued customer."
		#add company name
		message += "Regards,{}".format(mobile_money_settings.company)
			
		#get customer details
		customer_details_doc = frappe.get_list("Customer Details",filters ={
					'linked_customer_account':self.customer_account,
					'details_status':'Current'
				},
				fields = ['name','customer_phone_number','customer_email']
			)
		#get customer phone number
		customer_phone_number = customer_details_doc[0]['customer_phone_number']
		formated_number = "+254"+customer_phone_number[1:]
		#send notitification as a background job
		sms_instance = SMSClass()
		sms_instance.message_sending_handler(message,[formated_number])
		#mark notification as sent
		self.notification_sent = 1








