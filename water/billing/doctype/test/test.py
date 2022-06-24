# -*- coding: utf-8 -*-
# Copyright (c) 2022, Upande LTD. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document
from water.utils import QGIS

class Test(Document):
	# def on_update(self):
	# 	qgis_instance = QGIS(doc,'map_location')

	def after_save(self):
		pass
