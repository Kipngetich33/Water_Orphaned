# -*- coding: utf-8 -*-
# Copyright (c) 2021, Upande LTD. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from ....custom_methods.reusable_methods import validate_fields
from water.utils import enqueue_update_geometry_field

class CustomerDetails(Document):
	'''
	This is the customer details class
	'''
	def validate(self):
		'''
		Function that validates the document before
		it is saved
		'''
		#get meter reading setting
		self.get_required_settings()
		#validate billing area section
		self.validate_billing_area_section()
		#validate the connection details section
		self.validate_connection_details_section()
		#validate sanition details
		self.validate_sanition_details_section()
		#validate the gps coordinates section
		self.validate_gps_coordinates_section()

	def before_save(self):
		'''
		Function that runs before customer details document
		is saved
		'''
		#execute some actions based on state
		self.excecute_functions()
		#clear temporary values
		self.clear_temporary_values()

	def on_update(self):
		'''
		Function that runs once the document is saved
		'''
		enqueue_update_geometry_field(self,'map_location')
		
	def validate_billing_area_section(self):
		'''
		Function that validates the details in the billing
		area section
		'''
		#check if section status is transitioning
		if self.billing_area_transitioning:
			#check if details are confirmed
			if self.billing_area_confirmation == "Confirmed":
				#check requirement
				if self.meter_reading_settings.confirmation_requires_billing_area:
					#check billing area is given
					if self.billing_area:
						# check that the billing area is not a group
						area_doc = frappe.get_doc("Billing Area",self.billing_area)
						if area_doc.is_group:
							frappe.throw("The selected Billing Area cannot not be a group")
					else:
						frappe.throw("Billing Area field is required")

	def validate_connection_details_section(self):
		'''
		Function that validates the details in the connection
		details section
		'''
		#check if section is transitioning
		if self.connection_details_transitioning:
			if self.meter_status == "Connected":
				#check if connection requires meter
				if self.meter_reading_settings.connection_requires_meter:
					#check if meter is given
					if not self.meter:
						frappe.throw("The Meter field is required before connecting")
				#check installtion date is required
				if self.meter_reading_settings.connection_requires_installation_date:
					#check if date is given
					if not self.meter_installation_date:
						frappe.throw("The Installation Date is required before connecting")

				#check meter reading on installtion is required
				if self.meter_reading_settings.requires_meter_reading_on_installation:
					#check if reading is given
					if self.meter_reading_on_installation:
						#check that the given reading are either a float or integer
						try:
							float(self.meter_reading_on_installation)
						except:
							frappe.throw("The Meter reading should be a integer or a float")
					else:
						frappe.throw("The Meter Reading on Installation is required before connecting")

				#Ensure that a meter is not connected to another account
				meter_list = frappe.get_list('Customer Details',
                            filters = [['linked_customer_account','!=',self.linked_customer_account],
									['meter','=',self.meter],
									['details_status','=','Current']
								],
							fields = ['name']
						)
				#check if records were found
				if len(meter_list) > 0:
					frappe.throw('The selected meter is connected to another customer account')

	def validate_sanition_details_section(self):
		'''
		Function that validates the details in the sanitation
		details sections
		'''
		#required_titles
		type_of_sanitation = True
		onsite_category = False
		requires_type_of_septic = False
		requires_category_of_septic = False
		requires_septic_tank_accessibility = False
		type_of_pit_latrine = False
		category_of_pit_latrine = False

		#check if section is transitioning
		if self.sanitation_details_transitioning and \
		self.sanitation_details_confirmation == "Confirmed":
			#check requirements for type_of_sanitation
			if self.meter_reading_settings.requires_type_of_sanitation\
			and type_of_sanitation:
				#check of type is defined
				if self.onsite:
					onsite_category = True
				elif self.none:
					pass
				else:
					frappe.throw("Type of sanitation is required before confirmation")

			#check requirements for onsite_category 
			if self.meter_reading_settings.requires_onsite_category\
			and onsite_category:
				#check if category is defined
				if self.septic:
					requires_type_of_septic = True
					requires_category_of_septic = True
					requires_septic_tank_accessibility = True
				elif self.pit_latrine:
					type_of_pit_latrine = True
					category_of_pit_latrine = True
				else:
					frappe.throw("Onsite Category is required before confirmation")

			#check requirements for requires_type_of_septic
			if self.meter_reading_settings.requires_type_of_septic\
			and requires_type_of_septic:
				#check if type of septic is given
				if self.pour_flush_toilet_to_septic_tank or \
				self.flush_toilet_to_septic_tank:
					pass
				else:
					frappe.throw("Type of Spetic is required before confirmation")

			#check requirements for requires_category_of_septic
			if self.meter_reading_settings.requires_category_of_septic\
			and requires_category_of_septic:
				#check if category if septic is given
				if self.individual_septic or self.shared_septic:
					pass
				else:
					frappe.throw("Category of Septic is required before confirmation")

			#check requirements for requires_septic_tank_accessibility
			if self.meter_reading_settings.requires_septic_tank_accessibility\
			and requires_septic_tank_accessibility:
				#check if accessibility is defined
				if self.septic_tank_accessible_yes or self.septic_tank_accessible_no:
					pass
				else:
					frappe.throw("Accesibility to Septic tank should be defined before confirmation")

			#check requirements for type_of_pit_latrine
			if self.meter_reading_settings.requires_type_of_pit_latrine\
			and type_of_pit_latrine:
				#check if type is given
				if self.traditional_pit_latrine or \
				self.pit_latrine_with_slab or \
				self.ventilated_improved_pit_latrine or \
				self.composing_inlet:
					pass
				else:
					frappe.throw("Type of pit latrine required before confirmation")

			#check requirements for category_of_pit_latrine
			if self.meter_reading_settings.requires_category_type_of_pit_latrine\
			and category_of_pit_latrine:
				#check if category is given
				if self.individual_pit_latrine or self.shared_pit_latrine:
					pass
				else:
					frappe.throw("Category of pit latrine required before confirmation")

	def validate_gps_coordinates_section(self):
		'''
		Function that validates the gps_coordinates_section
		section
		'''
		if self.gps_coordinates_details_transitioning\
		and self.gps_coordinates_confirmed == "Confirmed":
			#check requires_gps_cordinates
			if self.meter_reading_settings.requires_gps_cordinates:
				if not self.gps_cordinates:
					frappe.throw("GPS cordinates field is required before confirmation")

			#check requires_gps_cordinates
			if self.meter_reading_settings.requires_gps_coordinate_of_the_meter_x:
				if not self.gps_coordinate_of_the_meter_x:
					frappe.throw("GPS Coordinate of the Meter X field is required before confirmation")

			#check requires_gps_coordinate_of_the_t_junction_y
			if self.meter_reading_settings.requires_gps_coordinate_of_the_t_junction_y:
				if not self.gps_coordinate_of_the_t_junction_y:
					frappe.throw("GPS Coordinate of the T Junction Y field is required before confirmation")

			#check requires_x
			if self.meter_reading_settings.requires_x:
				if not self.x:
					frappe.throw("X field is required before confirmation")

			#check requires_y
			if self.meter_reading_settings.requires_y:
				if not self.y:
					frappe.throw("Y field is required before confirmation")

			#check requires_latitude
			if self.meter_reading_settings.requires_latitude:
				if not self.latitude:
					frappe.throw("The Latitude field is required before confirmation")

			#check requires_y
			if self.meter_reading_settings.requires_longitude:
				if not self.longitude:
					frappe.throw("The Longitude field is required before confirmation")

			#check requires_altitude
			if self.meter_reading_settings.requires_altitude:
				if not self.altitude:
					frappe.throw("The Altitude field is required before confirmation")

			#check requires_altitude
			if self.meter_reading_settings.requires_accuracy:
				if not self.accuracy:
					frappe.throw("The Accuracy field is required before confirmation")
	
	def get_required_settings(self):
		'''
		Function that fetches the requiired settings and adds them
		as a class variable
		'''
		#get meter reading settings
		self.meter_reading_settings = frappe.get_single("Meter Reading Settings")
	
	def excecute_functions(self):
		'''
		Function that execute some functions on the 
		document before the document is saved
		'''
		if self.connection_details_transitioning:	
			#check if meter is disconnected
			if self.meter_status == "Disconnected"\
			and self.disconnection_level == 3:
				#clear connection fields
				self.meter = ""
				self.meter_installation_date = ""
				self.meter_reading_on_installation = ""
			
	def clear_temporary_values(self):
		'''
		Function that clears any temporary state values
		that should not be saved to the database
		'''
		#now unmark the transitioning billing area
		if self.billing_area_transitioning:
			self.billing_area_transitioning = 0
		#now unmark the transitioning connection section
		if self.connection_details_transitioning:
			self.connection_details_transitioning = 0
		#now unmark transitioning sanitation section
		if self.sanitation_details_transitioning:		
			self.connection_details_transitioning = 0
		#now unmark transitioning gps coordinates section
		if self.gps_coordinates_details_transitioning:
			self.gps_coordinates_details_transitioning = 0

def enqueue_long_job(doc,geo_field):
    frappe.enqueue('water.utils.update_geometry_field',doc=doc,geo_field=geo_field)
