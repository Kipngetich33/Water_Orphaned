# -*- coding: utf-8 -*-
# Copyright (c) 2021, Upande LTD. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class BillingArea(Document):
	'''
	Billing Area class document
	'''
	def validate(self):
		'''
		Function that validates the class
		instance before it is saved
		'''
		pass

	def before_save(self):
		'''
		Function that runs before the 
		document is saved
		'''
		#check or create root
		self.determine_creationg_of_root()
		#Add area title based on parent

	def determine_creationg_of_root(self):
		'''
		Function that determines the creation of a root
		billing area
		'''
		#checks whether billing area is root
		if not self.parent_billing_area:
			# check if another route exists
			route_area_list = frappe.get_list("Billing Area",
				filters={
					"root_area":["=",1],
					"name":["!=",self.name]
				},
			)
			#throw an area if it exist
			if route_area_list:
				frappe.throw("There can only be one root billing area")
			else:
				#mark this one as root
				self.root_area = 1
				self.is_group = 1

	def add_area_title_based_on_parent(self):
		'''
		Function the creates a title based on the given
		parent
		'''
		#check if bililling area has parent
		if self.parent_billing_area:
			pass


			


