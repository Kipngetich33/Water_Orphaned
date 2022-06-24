# -*- coding: utf-8 -*-
# Copyright (c) 2021, Upande LTD. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from sys import flags
import frappe
from frappe import database
from frappe.model.document import Document

class MeterReading(Document):
	'''
	This is the meter reading class
	'''
	def validate(self):
		'''
		Function that validates that all the required details
		are added before 
		'''
		#run consumption function before validation
		self.calculate_consumption()
		#validate_single_meter_reading_doc
		self.validate_single_meter_reading_doc()
		#now validate values
		self.validate_values()
		
	def before_save(self):
		'''
		Function that runs before the document is saved
		'''
		#add last_meter_reading if none exists
		self.get_latest_reading_for_meter()
		#calculate consumption
		self.calculate_consumption()
		#mark as latest meter reading
		self.mark_as_latest_meter_reading()

	def on_update(self):
		'''
		Function that runs before the document is
		saved
		'''
		#update the last meter reading doc
		self.update_last_meter_reading_doc()
		#update the linked meter reading sheet
		self.update_meter_reading_sheet()

	def get_latest_reading_for_meter(self):
		'''
		Function that gets latest reading for the current 
		meter
		'''
		#return is latest meter reading is already defined
		if self.last_meter_reading:
			return 
		
		#find a previous meter reading
		meter_reading_list = frappe.get_list("Meter Reading",
			filters = [
				['latest_readings_for_meter','=',1],
				['meter','=',self.meter],
				['name','!=',self.name],
			],
			fields = ['*']
		)

		#check if any meter readings were found
		if meter_reading_list:
			#get the first reading on the list
			self.last_meter_reading = meter_reading_list[0]['current_meter_reading']
			#add the last meter reading doc where readings were sourced
			self.last_reading_doc =  meter_reading_list[0]['name']
		else:
			#get readings from customer details
			customer_doc_list = frappe.get_list("Customer Details",
				filters =  {
					'meter':self.meter,
					'details_status':'Current'
				},
				fields = ['name','meter_reading_on_installation']
			)
			#check if document is associated with a customer account
			if customer_doc_list:
				#get reading on meter reading
				self.last_meter_reading = float(customer_doc_list[0]['meter_reading_on_installation'])
			else:
				frappe.throw("A Cutomer Details document associated with the meter {}\
					does not exist".format(self.meter))

	def calculate_consumption(self):
		'''
		Function that uses last meter reading 
		and the current readings to calulate
		consumption
		'''
		# if self.last_meter_reading and self.current_meter_reading:
		last_meter_reading = 0
		current_meter_reading = 0
		if self.last_meter_reading:
			last_meter_reading = self.last_meter_reading
		if self.current_meter_reading:
			current_meter_reading = self.current_meter_reading
		consumption = current_meter_reading - last_meter_reading
		#check if curent consumption is equals to calculated
		if self.consumption != consumption:
			self.consumption = consumption

	def mark_as_latest_meter_reading(self):
		'''
		Function that marks the current meter reading as the latest
		'''
		self.is_new_doc = False
		#check if the meter reading is new
		if not frappe.db.exists("Meter Reading",self.name):
			#mark the current document as the latest meter reading
			self.latest_readings_for_meter = 1
			self.is_new_doc = True

	def update_last_meter_reading_doc(self):
		'''
		Function that unmarks the last meter reading so that the
		current once becomes the most current
		'''
		#check if document is new else return
		if not self.is_new_doc:
			return
		#check if the last reading doc is defined else return
		if not self.last_reading_doc:
			return 
		#checks passed hence close the previous meter reading
		last_reading_doc = frappe.get_doc("Meter Reading",self.last_reading_doc)
		if last_reading_doc.latest_readings_for_meter:
			last_reading_doc.latest_readings_for_meter = 0
			#save changes to database
			last_reading_doc.save(ignore_permissions = True)
			frappe.db.commit()

	def update_meter_reading_sheet(self):
		'''
		Function that updates the last meter reading if 
		any is linked
		'''
		#check if meter reading is linked to a reading sheet
		meter_reading_detail_list = frappe.get_list("Meter Reading Sheet Detail",
			filters = [
				['meter_reading','=',self.name]
			],
			fields = ['*']
		)	
		#now loop through the the list
		for meter_reading_detail in meter_reading_detail_list:
			#get the reading sheet detail doctype
			detail_doc = frappe.get_doc("Meter Reading Sheet Detail",meter_reading_detail['name'])
			detail_doc.status = self.status
			detail_doc.current_meter_reading = self.current_meter_reading
			detail_doc.consumption = self.consumption
			#save the detail doc
			detail_doc.save(ignore_permissions = True)
			frappe.db.commit()

	def validate_single_meter_reading_doc(self):
		'''
		Function that checks to ensure that there can 
		be only one open meter reading doc per meter
		at a time
		'''
		if frappe.db.exists("Meter Reading",self.name):
			#existing doc
			pass
		else:
			#new document
			open_reading_list = frappe.get_list("Meter Reading",
				filters = [
					['status','=','Open'],
					['meter','=',self.meter],
					['name','!=',self.name],
				],
				fields = ['*']
			)
			#check meter reading exist
			if open_reading_list:
				#get meter readidn url
				doc = frappe.get_doc("Meter Reading",open_reading_list[0]['name'])
				frappe.throw("There is already an open <a href='{}'>Meter Reading</a>\
					Document for the Meter {}".format(doc.get_url().replace(" ","%20"),
					self.meter)
				)

	def validate_values(self):
		'''
		Function that checks that all the required values
		are given based on current status
		'''
		#initialize irregular readings as false
		self.irregular_readings = False
		if self.status == 'Closed':
			#check for irregular readings
			if self.last_meter_reading <= 0\
			or self.current_meter_reading <= 0\
			or self.consumption <= 0:
				self.irregular_readings = True
			#check if readings are irregular
			if self.irregular_readings:
				#check if they have been confirmed
				if self.confirm_irregular_reading\
				and self.reason_for_irregular_reading:
					pass
				else:
					frappe.throw("This meter reading has irregular values.Please check\
						and confirm in order to continue")

		
