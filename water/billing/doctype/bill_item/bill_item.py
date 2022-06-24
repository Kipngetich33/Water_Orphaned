# -*- coding: utf-8 -*-
# Copyright (c) 2021, Upande LTD. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from redis.client import parse_sentinel_slaves_and_sentinels

class BillItem(Document):
	'''
	This is the bill items doctype class
	'''
	def validate(self):
		'''
		Functiont that validates the Bill Item 
		doctype
		'''
		pass

	def before_save(self):
		#check or create ERP item
		self.check_or_create_item()

	def on_update(self):
		'''
		Function that runs when the Document
		is saved 
		'''
		#update item values
		self.update_item_values()
		pass
		
	def check_or_create_item(self):
		'''
		Function that checks that a corresponding 
		ERPNext item exist else create one
		'''
		#if item has no linked ERP item create one
		if not self.linked_erp_item:
			item_list = frappe.get_list("Item",filters={
				'name':self.name
			})
			#check if any item was found
			if len(item_list) > 0:
				#link it to current bill item
				self.linked_erp_item = item_list[0]['name']
			else:
				#create new item
				item_doc = frappe.new_doc("Item")
				item_doc.item_name = self.name
				item_doc.item_code = self.name
				item_doc.item_group = "Services"
				item_doc.stock_uom = "Cubic Meter"
				item_doc.standard_rate = self.amount
				item_doc.description = "Water Tarrif Item {}\
				".format(self.name)
				#now save the item
				item_doc.save(ignore_permissions = True)
				frappe.db.commit()
				#link it to current bill item
				self.linked_erp_item = item_doc.name
				
	def update_item_values(self):
		'''
		Function that updates values for the bill 
		item
		'''
		#get item price
		price_doc_list = frappe.get_list("Item Price",filters = {
			'item_code':self.name,
			'item_name':self.name,
		})
		if price_doc_list:
			#get the first item
			item_price_name = price_doc_list[0]['name']
			item_price_doc = frappe.get_doc("Item Price",item_price_name)
			#values to update
			if item_price_doc.price_list_rate == self.amount:
				pass
			else:
				item_price_doc.price_list_rate = self.amount
				#now save the item
				item_price_doc.save(ignore_permissions = True)
				frappe.db.commit()
		
		



