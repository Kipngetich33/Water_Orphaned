# -*- coding: utf-8 -*-
# Copyright (c) 2021, Upande LTD. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

import datetime

class BillingPeriod(Document):
	'''
	Billing Period document class
	'''
	def validate(self):
		'''
		Function that validates the Billing Period
		document
		'''
		
		#start canno be greater than end date
		self.validate_start_n_end_dates()
		#check that billing periods do not overlap
		self.billing_period_does_not_overlap()

	def validate_start_n_end_dates(self):
		'''
		Function that checks that the startdate cannot be 
		greater thatn the enddate
		'''
		# start date should be less that end date
		if self.start_date <= self.end_date:
			pass
		else:
			frappe.throw("The <strong>Start Date</strong> cannot\
				be greater than the <strong>End Date</strong>")

	def billing_period_does_not_overlap(self):
		'''
		Functiion that checks that the billing period
		duration does not overlap with the duration of 
		other periods
		'''
		# ensure the period does not overlap with the duration of
		# another billing period
		if type(self.start_date) and type(self.end_date):
			new_start_date = self.start_date
			new_end_date = self.end_date
		else:
			new_start_date = datetime.datetime.strptime(self.start_date, '%Y-%m-%d')
			new_end_date = datetime.datetime.strptime(self.end_date, '%Y-%m-%d')
		
		# get overlapping dates
		period_with_overlapping_dates = frappe.db.sql("""select name from \
			`tabBilling Period` where '{}' between start_date and end_date || \
			'{}' between start_date and end_date""".format(new_start_date,new_end_date))
		
		if len(period_with_overlapping_dates) > 0:
			# loop to check if any is not the same as the current year
			for period in period_with_overlapping_dates:
				if period[0] != self.name:
					frappe.throw("<strong>Start</strong> and <strong>End Dates</strong> \
						of this Billing Period overlap with those of <strong>{}</strong>\
						".format(period[0]))
