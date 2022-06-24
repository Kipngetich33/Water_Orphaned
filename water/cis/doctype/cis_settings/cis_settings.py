# -*- coding: utf-8 -*-
# Copyright (c) 2021, Upande LTD. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from ...cis_custom_methods import fetch_cis_from_ona

class CISSettings(Document):
	'''
	The CISSettings class
	'''
	def validate(self):
		'''
		Function that validates the CISSettings Settings
		document before it is saved
		'''
		# run the final_execute_function_before_saving before saving
		pass

	def on_update(self):
		# check if user is requesting to pull new entries
		if self.fetching_new_entries:
			fetch_cis_from_ona()
	
	

