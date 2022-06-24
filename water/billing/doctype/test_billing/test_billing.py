# -*- coding: utf-8 -*-
# Copyright (c) 2022, Upande LTD. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from water.utils import QGIS

class TestBilling(Document):
	def on_update(self):
		print('*'*80)
		enqueue_long_job(self,'location')

def update_geojson(doc,geo_field):
	print("on update")
	print("updateing the thing")
	instance = QGIS(doc,'location')
	instance.main()

def enqueue_long_job(doc,geo_field):
    frappe.enqueue('water.billing.doctype.test_billing.test_billing.update_geojson',doc=doc,geo_field=geo_field)