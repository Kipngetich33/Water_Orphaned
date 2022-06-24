# -*- coding: utf-8 -*-
# Copyright (c) 2021, Upande LTD. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

#app imports
from ....custom_methods.reusable_methods import create_bill


class BillingActions(Document):
	'''
	Billign Action document class
	'''
	def validate(self):
		'''
		Functiont that validates the Billing Action
		document before it is saved
		'''
		self.validated_selected_meter_reading_sheet()

	def before_save(self):
		'''
		Functiont that runs before the document is saved
		'''
		#create a bill for every meter reading
		self.create_bills_for_meter_reading_sheet()
		#mark sheet as billed
		self.mark_sheet_as_biled()

	def validated_selected_meter_reading_sheet(self):
		'''
		Function that checks that the selected meter
		readign sheet passes all the requires for billing
		'''
		#if not reading sheet or billing_the_sheet return
		if not self.meter_reading_sheet or not\
		self.billing_the_sheet:
			return 
		#get the meter readign sheet document
		self.sheet_doc = frappe.get_doc("Meter Reading Sheet",self.meter_reading_sheet)
		#check that the reading sheet is closed 
		if self.sheet_doc.status != 'Closed':
			frappe.throw("Billing is only allowed for closed meter reading sheets")
		#check if readign has not already been billed
		if self.sheet_doc.billed:
			frappe.throw("The selected meter reading sheet has already been billed")

	def create_bills_for_meter_reading_sheet(self):
		'''
		Function that creates bills to for the selected meter reading
		sheet
		'''
		#if not reading sheet or billing_the_sheet return
		if not self.meter_reading_sheet or not\
		self.billing_the_sheet:
			return

		#loop through meter readings in sheet
		for meter_reading in self.sheet_doc.meter_reading_sheet_detail:
			self.extra_fields = [
				{'field':'customer','value':meter_reading.erpnext_customer},
				{'field':'last_meter_reading','value':meter_reading.last_meter_reading},
				{'field':'current_meter_reading','value':meter_reading.current_meter_reading},
				{'field':'consumption','value':meter_reading.consumption}
			]
			#initialize the bill item details
			self.bill_items_details = []
			#set meter rent and tarrifs if none is already available
			self.fetching_tarrifs_n_standing_charges(meter_reading.customer_type)
			#add meter rent to bill_items_details
			self.generate_standing_charge_bill_item(meter_reading.customer_type)
			#add water tariffs to bill_items_details
			self.generate_water_tarrif_items(meter_reading)
			#use reusable method to create bill
			create_bill(meter_reading.customer_account,"Water Bill",self.bill_items_details,self.extra_fields)
			
	def fetching_tarrifs_n_standing_charges(self,customer_type):
		'''
		Function that feches all the water tarrifs,standing charges and any
		other applicable monthly fees applicable to a given cutomer type
		input:
			customer_type - str
		'''
		#check if tarrifs and rent for customer is already defined
		if hasattr(self,customer_type):
			return
			
		#get bill items for customer type
		list_of_bill_items = frappe.get_list("Bill Item",filters = {
				'customer_type':customer_type,
			},
			fields = ['name','start_reading','end_reading',
			'bill_type','flat_rate']
		)
		#sort the items to get tarrifs
		list_of_tarrifs = list(filter(lambda x: x['bill_type'] == 'Tariff',list_of_bill_items))
		#sort them per start value
		sorted_list_of_tarrifs = sorted(list_of_tarrifs, key=lambda k: k['start_reading'])
		#sort the items to get meter rent
		list_of_standing_charges = list(filter(lambda x: x['bill_type'] == 'Standing Charge',list_of_bill_items))

		#please find a way to fix the issue of standing charge out of index if no standing charge has been added in the system
		standing_charge = list_of_standing_charges[0] 
	
		#now set customer tarrif and meter rent attribute
		setattr(self,customer_type,{
				'sorted_tariffs':sorted_list_of_tarrifs,
				'Standing Charge':standing_charge
			})

	def generate_standing_charge_bill_item(self,customer_type):
		'''
		Function that generates bill item for monthly standing
		charge
		input:
			customer_type - str
		'''
		standing_charge = getattr(self,customer_type)['Standing Charge']
		# add items to self.bill_items_details
		self.bill_items_details.append({
			'bill_item':standing_charge['name'],
			'quantity':1
		})

	def generate_water_tarrif_items(self,meter_reading):
		'''
		Function that generates bill item for water tariff rates
		based on given readings
		input:
			customer_type - str
		'''
		#initialize readings as the given readings
		consumption = meter_reading.consumption
		#get all applicable customer tariffs
		tariff_list = getattr(self,meter_reading.customer_type)['sorted_tariffs']
		#now loop throug the tariff_list
		for tariff in tariff_list:
			#check its end readings is defined
			if tariff['end_reading']:
				#subtract to get consumption within this tariff
				#check if consumption is greater than tariff['end_reading']
				if consumption > tariff['end_reading']:
					tariff_consumption = tariff['end_reading'] - tariff['start_reading']
				else:
					#this is the highest applicable tariff to readings
					tariff_consumption = consumption - tariff['start_reading']
			else:
				#this the highest available tarriff
				tariff_consumption = consumption - tariff['start_reading']
			#now add items
			if tariff_consumption <= 0:
				break #break the loop
			else:
				if tariff['flat_rate'] == "Yes":
					defined_quantity = 1
				else:
					defined_quantity = tariff_consumption
				# add items to self.bill_items_details
				self.bill_items_details.append({
					'bill_item':tariff['name'],
					'quantity':defined_quantity
				})

	def mark_sheet_as_biled(self):
		'''
		Function that marks the current meter reading sheet as 
		billed so that it is not billed twice
		'''
		#if no reading sheet is selected or not billing_the_sheet 
		if not self.meter_reading_sheet or not\
		self.billing_the_sheet:
			return

		#mark the current sheet as billed
		self.sheet_doc.billed = 1
		self.sheet_doc.save(ignore_permissions = True)
		frappe.db.commit()
		#unmark action fields
		self.meter_reading_sheet = ""
		self.billing_the_sheet = 0




			
	
		


			                                                                                                                                                                                                                                                  

		

	






