# -*- coding: utf-8 -*-
# Copyright (c) 2021, Upande LTD. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from ....custom_methods.reusable_methods import get_non_group_billing_areas\
	,get_customers_of_billing_area

class MeterReadingSheet(Document):
	'''
	This is the meter reading document class
	'''
	def validate(self):
		'''
		Class validation function
		'''
		#validate the meter reading table
		if not len(self.meter_reading_sheet_detail)\
		and not self.fetching_meter_readings:
			frappe.throw("The Meter Reading Table cannot be empty")
		#validate the meter reading command
		if self.fetching_meter_readings:
			#get meter reading list
			if len(self.meter_reading_sheet_detail):
				frappe.msgprint("You have already fetched meter readings")
		#checks that all the reading are for closing
		self.validate_for_closing()

	def before_save(self):
		'''
		Function that runs before the document is saved
		'''
		print('*'*80)
		print("before saving:")
		#check that the billing area is not a group
		area_doc = frappe.get_doc("Billing Area",self.billing_area)
		if area_doc.is_group:
			frappe.throw("The selected Billing Area cannot not be a group")

		#command to fetch meter readings
		if self.fetching_meter_readings and\
		not self.meter_reading_sheet_detail:
			print('ready to pick')
			#get non group billing areas
			self.billing_areas = get_non_group_billing_areas(self.billing_area)
			#initialize applicable customers as empty list
			self.applicable_customers = []
			#loop through billing areas
			for billing_area in self.billing_areas:
				#get customers within billing areas
				customer_per_area = get_customers_of_billing_area(billing_area)
				self.applicable_customers += customer_per_area

			print('all customers',self.applicable_customers)

			#loop through applicable customers
			for customer in self.applicable_customers:
				#get or create meter readings
				meter_reading = self.check_or_create_reading(customer)
				
				print("meter reading found :",meter_reading)
				if meter_reading['status']:
					row = self.append("meter_reading_sheet_detail", {})
					#check if type is dict
					if type(meter_reading['meter_reading_doc']) == dict:
						meter_reading['meter_reading_doc']['name']
					else:				
						row.meter_reading = meter_reading['meter_reading_doc'].name
						row.meter_serial = meter_reading['meter_reading_doc'].meter
						row.customer_name = meter_reading['customer_name']
						row.customer_type = meter_reading['customer_type']
						row.customer_account = meter_reading['customer_account']
						row.erpnext_customer = meter_reading['erpnext_customer']
						row.last_meter_reading = meter_reading['meter_reading_doc'].last_meter_reading
						row.current_meter_reading = meter_reading['meter_reading_doc'].current_meter_reading
						row.consumption = meter_reading['meter_reading_doc'].consumption
						row.status = meter_reading['meter_reading_doc'].status
			
			print(self.meter_reading_sheet_detail)

		#now unmark the action fields
		if self.fetching_meter_readings:
			self.fetching_meter_readings = 0
				
	def on_update(self):
		'''
		Function that runs when the meter reading document 
		is saved
		'''
		if not len(self.meter_reading_sheet_detail):
			frappe.msgprint("No active customers were found in the selected Billing Area")

	def check_or_create_reading(self,customer_details):
		'''
		Function that creates a new meter reading document
		for a meter
		'''
		print("chekng or creating")
		#check if customer is currently Active
		if customer_details['status'] == "Active":
			print("customer active")
			#check if there is an existing open doc
			list_of_meter_readings = frappe.get_list("Meter Reading",filters = {
					'meter':customer_details['meter'],
					'status':'Open'
				},
				fields = ["*"]
			)
			#check another already exists
			if len(list_of_meter_readings) > 0:
				#get the first
				return {'status':True,
					'meter_reading_doc':list_of_meter_readings[0],
					'customer_name':customer_details['customer_full_name'],
					'customer_type':customer_details['customer_type'],
					'customer_account':customer_details['linked_customer_account'],
					'erpnext_customer':customer_details['customer']
				}
			else:
				#create a new meter reading
				meter_reading_doc = frappe.new_doc("Meter Reading")
				meter_reading_doc.meter = customer_details['meter'] 
				#now save document to database
				meter_reading_doc.save(ignore_permissions = True)
				frappe.db.commit()
				#return the meter reading document
				return {'status':True,
					'meter_reading_doc':meter_reading_doc,
					'customer_name':customer_details['customer_full_name'],
					'customer_type':customer_details['customer_type'],
					'customer_account':customer_details['linked_customer_account'],
					'erpnext_customer':customer_details['customer']
				}
		else:
			#return status as false
			return{'status':False}

	def validate_for_closing(self):
		'''
		Function that checks that the meter readings
		are validate before closing
		'''
		#if meter reading is not being closed return
		if self.status != "Closed":
			return 

		#checks that all the reading in the meter reading sheet are closed
		for meter_detail in self.meter_reading_sheet_detail:
			if meter_detail.status != "Closed":
				frappe.throw("The Meter Reading {} for the customer {} is still Open.<hr>\
					All Meter Readings need to be closed in order to close the reading sheet\
					".format(meter_detail.name,meter_detail.customer_name))
		

