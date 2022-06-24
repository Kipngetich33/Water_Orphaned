# -*- coding: utf-8 -*-
# Copyright (c) 2021, Upande LTD. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document

class BillingSettings(Document):
	def before_save(self):
		"""set the reference_doctype as empty ready for selection
		of another doctype and an action be run using it"""
		self.reference_doctype = ""
