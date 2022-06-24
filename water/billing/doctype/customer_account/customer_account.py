# -*- coding: utf-8 -*-
# Copyright (c) 2021, Upande LTD. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

#app imports
from ....custom_methods.reusable_methods import validate_fields,error_handler
from ....custom_methods.connection import initiate_new_connection,initiate_acc_activation,\
	initiate_acc_disconnection,validate_account_connection,validate_account_activation,\
	validate_account_disconnection,initiate_acc_activation,initiate_account_reconnection,\
	validate_account_reconnection,initiate_permanent_acc_disconnection\
	,validate_permanent_account_disconnection

class CustomerAccount(Document):
	'''
	This is the customer class
	'''
	def validate(self):
		'''
		Function that validates the document before
		it is saved 
		'''
		#add the billing settings to the class 
		self.get_required_settings()
		# list of all required fields
		required_fields_list = [
            {'field_name':'Full Name','value':self.full_name,'data_type':str,'saving_required':1},
			{'field_name':'Phone Number','value':self.phone_number,'data_type':str,'saving_required':1},
			{'field_name':'ID Number','value':self.id_no,'data_type':str,'saving_required':1},
			{'field_name':'Customer Type','value':self.customer_type,'data_type':str,'saving_required':1},
		]
		#only validate fields if status is not draft
		if self.status != "Draft":
			#validate the fields
			validation_status = validate_fields(required_fields_list)
			#check validation status
			error_handler(validation_status)
		#now validate document based on statuses
		self.validate_based_on_status()

	def before_save(self):
		'''
		Function that runs before the document is saved
		'''
		#check account number addition
		self.check_of_create_name()
		#check action based on status
		if self.status == "Pending Connection":
			#check of create a customer details doc
			self.check_or_create_cus_details()
			#create a customer account in ERPnext
			self.check_or_create_customer()

		if self.status == "Pending Activation":
			pass

		#call an activity based on status to transition customers
		self.initiate_activity_based_on_status()
		#execute some action based on the document status
		self.execute_some_action_based_on_statatus()

	def on_update(self):
		self.update_customer_details_status()
		
	def get_required_settings(self):
		'''
		Function that fetches the required settings and adds them
		as a class variable
		'''
		#if the account status is draft return
		if self.status == "Draft":
			return

		#create customer bills#check if billing settings has been loaded
		try:
			self.billing_settings
		except:
			#get correct billing setting from Billing Items
			try:
				self.billing_settings = frappe.get_doc("Billing Settings Item",self.customer_type)
			except:
				frappe.throw("A Billing Settings Item for {} does not exist"\
					.format(self.customer_type))

	def validate_based_on_status(self):
		'''
		Function that runs validation based on the specific
		status of the document
		'''
		#check if the document status is transitioning
		if self.status_transitioning:
			#validate before connection
			if self.status == "Connected":
				#check the previous status
				if self.previous_status == "Pending Connection":
					if not self.registration_complete:
						#validate account connection
						validate_account_connection(self)
					else:
						#validate account reconnection
						validate_account_reconnection(self)

			#validate before activation
			if self.status == "Active":
				#check the previous status
				if self.previous_status == "Pending Activation":
					#validate account connection
					validate_account_activation(self)

			#validate before disconnection
			if self.status == "Disconnected":
				#check the previous status
				if self.previous_status == "Pending Disconnection":
					#validate account disconnection
					validate_account_disconnection(self)

			#validate before disconnection
			if self.status == "Dormant":
				#check the previous status
				if self.previous_status == "Pending Permanent Disconnection":
					#validate account disconnection
					validate_permanent_account_disconnection(self)

	def check_or_create_cus_details(self):
		'''
		Function that checks if a details document 
		exist for a customer account or else create 
		a new one
		'''
		#check or create a new customer details document
		if not self.customer_details:
			#check if a customer details document exists
			customer_details = frappe.get_list('Customer Details',
								filters = {
									'details_status':'Current',
									'linked_customer_account':self.name
								},
								fields = ['name']
							)
			if len(customer_details) > 0:
				#set the customer details doc
				self.customer_details = customer_details[0].name
			else:
				#create a new customer details document
				customer_details_doc = frappe.new_doc("Customer Details")
				customer_details_doc.linked_customer_account = self.name
				customer_details_doc.customer_full_name = self.full_name
				customer_details_doc.customer_phone_number = self.phone_number
				customer_details_doc.id_number = self.id_no
				customer_details_doc.customer_type = self.customer_type
				#save to database
				customer_details_doc.save(ignore_permissions=True)
				frappe.db.commit()
				#now set the customer details account
				self.customer_details = customer_details_doc.name

	def check_or_create_customer(self):
		'''
		Function that checks if a details document 
		exist for a customer account or else create 
		a new one
		'''
		#check or create a new customer details document
		if self.customer_details:
			#get customer details doc
			cus_details_doc = frappe.get_doc("Customer Details",self.customer_details)
			#check if customer account does not already exist
			if not cus_details_doc.customer:
				#create a new customer
				erp_cus_doc = frappe.new_doc("Customer")
				erp_cus_doc.customer_name = self.full_name
				#save to database
				erp_cus_doc.save(ignore_permissions=True)
				frappe.db.commit()
				#now set the customer details account
				cus_details_doc.customer = erp_cus_doc.name
				#save new details as well
				cus_details_doc.save(ignore_permissions=True)
				frappe.db.commit()

	def initiate_activity_based_on_status(self):
		'''
		A function that initiates a specific activity
		depending on the status of the document
		'''
		#check if the document status is transitioning
		if self.status_transitioning:	
			if self.status == "Pending Connection":
				#check the previous status
				if self.previous_status == "Draft":
					#initiate new connection
					initiate_new_connection(self)

			if self.status == "Pending Connection":
				#check the previous status
				if self.previous_status == "Disconnected" \
				or self.previous_status == "Dormant":
					#initiate reconnection
					initiate_account_reconnection(self)
			
			if self.status == "Pending Activation":
				#check the previous status
				if self.previous_status == "Connected":
					#initiate account activation
					initiate_acc_activation(self)

			if self.status == "Pending Disconnection":
				#check the previous status
				if self.previous_status == "Active":
					#initiate account activation
					initiate_acc_disconnection(self)

			if self.status == "Pending Permanent Disconnection":
				#check the previous status
				if self.previous_status == "Disconnected":
					#initiate account activation
					initiate_permanent_acc_disconnection(self)

	def execute_some_action_based_on_statatus(self):
		'''
		Functions that runs some functionality depending on 
		document status
		'''
		#check if the document status is transitioning
		if self.status == "Active" and not self.registration_complete:
			self.registration_complete = 1

	def update_customer_details_status(self):
		'''
		Function that updates the customer details status
		'''
		if self.customer_details:
			customer_details_doc = frappe.get_doc("Customer Details",self.customer_details)
			#check if current status and status on customer details match
			if self.status == customer_details_doc.status:
				pass
			else:
				customer_details_doc.status = self.status
			#now save to database
			customer_details_doc.save(ignore_permissions = True)
			frappe.db.commit()

	def check_of_create_name(self):
		'''
		Function that checks if an account number is given for a user
		then sets that account number as the the name of the account
		'''
		#check if the document is already saved
		if not frappe.db.exists("Customer Account", self.name):
			#check if an account number if given
			if self.custom_account_number:
				self.name = self.custom_account_number

