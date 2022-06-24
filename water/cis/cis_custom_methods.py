from __future__ import unicode_literals
from functools import reduce 

# std lib imports
import requests,json,datetime,json,datetime
import frappe

# the list below contains a list of fields that are contained in the Ona form 
# and the corresponding name of the  those fields in the CIS Data doctype
list_of_ona_fields_to_cis_data = {'_id':'_id',
	'collector_name':'service_area_details/collector_name',
	'date':'date',
	'zone':'service_area_details/zone',
	'sub_zone':'service_area_details/sub_zone',
	'type_of_housing':'housing_details/housing_type',
	'type_of_premises':'housing_details/premise_type',
	'type_of_residential_or_mixed_premise':'housing_details/domestic_house_types',
	'number_of_people_in_the_household':'housing_details/number_of_people_in_household',
	'type_of_commercial_premise':'housing_details/commercial_types',
	'type_of_institution':'housing_details/institution_types',
	'type_of_health_facility':'housing_details/health_facility',
	'category_of_health_facility':'housing_details/category_of_health_facilty',
	'category_of_institution':'housing_details/institution_category',
	'number_of_people_in_institution':'housing_details/number_of_people_in_institution',
	'email_of_the_institution':'housing_details/company_email',
	'average_number_of_people_served_at_the_fontenerio_per_day':'housing_details/average_no_of_pple_served_by_kiosk_perday',
	'first_name_landlord':'landlord_address/first_name_landlord',
	'land_lord_or_owner_surname':'landlord_address/surname_landlord',
	'land_lord_or_owner_cell':'landlord_address/owner_address_cell',
	'customer_details_same_as_landlord':'details_title/address_of_connection_same',
	'different_customer_name':'details_title/connection_address/connection_address_name',
	'different_customer_cell':'details_title/connection_address/customer_address_cell',
	'does_customer_have_a_connection':'details_title/customer_connected',
	'customer_have_a_connection':'details_title/account_known',
	'account_no':'details_title/account_information/account_group/account_no',
	'account_name':'details_title/account_information/account_group/account_name',
	'total_number_of__households_in_the_mdu':'details_title/account_information/number_of_people_in_multi_dwelling_household_',
	'average_number_of_people_in_each_household_':'details_title/account_information/average_number_of_people_in_each_household_',
	'billing_status':'details_title/account_information/billing_status',
	'why_customer_is_not_billed':'details_title/account_information/why_customer_is_not_billed',
	'frequency_of_bill_delivery':'details_title/account_information/bill_info/frequency_of_bill_2',
	'connection_status':'details_title/account_information/bill_info/connection_status',
	'how_often_do_you_receive_water':'details_title/account_information/bill_info/connection_details/how_often_do_you_receive_water',
	'days_with_supply':'details_title/account_information/bill_info/connection_details/days_with_supply',
	'daily_hours':'details_title/account_information/bill_info/connection_details/daily_hours',
	'hours_with_supply_daily':'details_title/account_information/bill_info/connection_details/hours_with_supply_daily',
	'last_time_to_receive_water':'details_title/account_information/bill_info/connection_details/last_time_to_receive_water',
	'storage_tank_available':'details_title/account_information/bill_info/connection_details/storage_tank_available',
	'storage_tank_location':'details_title/account_information/bill_info/connection_details/storage_tank_location',
	'storage_tank_size':'details_title/account_information/bill_info/connection_details/storage_tank_size',
	'disconnection_duration':'details_title/account_information/bill_info/disconnection_duration',
	'water_sources':'details_title/account_information/bill_info/water_sources',
	'name_of_sssp':'details_title/account_information/bill_info/name_of_sssp',
	'name_community_project_':'details_title/account_information/bill_info/name_community_project',
	'water_connection':'details_title/account_information/bill_info/water_connection',
	'meter_location':'details_title/account_information/bill_info/connection_available_grp/meter_location',
	'why_access_to_meter_location_is_denied':'details_title/account_information/bill_info/connection_available_grp/why_access_to_meter_location_is_denied',
	'meter_status':'details_title/account_information/bill_info/connection_available_grp/meter_status',
	'meter_settlement':'details_title/account_information/bill_info/connection_available_grp/meter_settlement',
	'meter_material':'details_title/account_information/bill_info/connection_available_grp/meter_info/meter_info_a/meter_body/meter_material',
	'inlet_pipe_size':'details_title/account_information/bill_info/connection_available_grp/meter_info/meter_info_a/inlet_pipe_size',
	'meter_size':'details_title/account_information/bill_info/connection_available_grp/meter_info/meter_info_a/meter_size',
	'meter_position':'details_title/account_information/bill_info/connection_available_grp/meter_info/meter_info_a/meter_position',
	'meter_flow_direction':'details_title/account_information/bill_info/connection_available_grp/meter_info/meter_info_a/meter_flow_direction',
	'item':'details_title/account_information/bill_info/connection_available_grp/meter_info/meter_info_a/accessories_group/accessories_label',
	'valve_before_meter':'details_title/account_information/bill_info/connection_available_grp/meter_info/meter_info_a/accessories_group/valve_before_meter',
	'valve_after_meter':'details_title/account_information/bill_info/connection_available_grp/meter_info/meter_info_a/accessories_group/valve_after_meter',
	'meter_seal':'details_title/account_information/bill_info/connection_available_grp/meter_info/meter_info_a/accessories_group/meter_seal',
	'connection_seal':'details_title/account_information/bill_info/connection_available_grp/meter_info/meter_info_a/accessories_group/connection_seal',
	'meter_liners':'details_title/account_information/bill_info/connection_available_grp/meter_info/meter_info_a/accessories_group/meter_liners',
	'pipe_material':'details_title/account_information/bill_info/connection_available_grp/meter_info/meter_info_a/pipe_material',
	'state_of_the_meter':'details_title/account_information/bill_info/connection_available_grp/meter_info/meter_info_a/meter_state',
	'meter_brand':'details_title/account_information/bill_info/connection_available_grp/meter_info/meter_info_a/meter_brand',
	'meter_serial_no':'details_title/account_information/bill_info/connection_available_grp/meter_info/meter_info_a/meter_no',
	'meter_class':'details_title/account_information/bill_info/connection_available_grp/meter_info/meter_info_a/meter_class',
	'readings_of_the_meter':'details_title/account_information/bill_info/connection_available_grp/meter_info/meter_info_a/meter_readings',
	'metering_problems':'details_title/account_information/bill_info/connection_available_grp/metering_problems',
	'meter_read_monthly':'details_title/account_information/bill_info/connection_available_grp/meter_read_monthly',
	'installation_date_known':'details_title/account_information/bill_info/connection_available_grp/installation_date_known',
	'tentative_year_of_installation':'details_title/account_information/bill_info/connection_available_grp/tentative_year_of_installation',
	'installation_date':'details_title/account_information/bill_info/connection_available_grp/installation_date',
	'customer_willing_to_be_connected':'details_title/customer_willing_to_be_connected',
	'approximate_distance':'details_title/approximate_distance',
	'number_of_people_in_multi_dwelling_household':'details_title/number_of_people_in_multi_dwelling_household',
	'average_number_of_people_in_each_household':'details_title/average_number_of_people_in_each_household',
	'water_source':'details_title/water_source',
	'name_of_sssp_':'details_title/name_of_sssp',
	'name_community_project':'details_title/name_community_project',
	'other_alternative_source':'details_title/water_sources_other',
	'type_of_sanitation':'sanitation_group/type_of_sanitation',
	'onsite_category':'sanitation_group/onsite_category',
	'choose_type_of_pit_latrine':'sanitation_group/pit_latrine',
	'category_type_of_pit_latrine':'sanitation_group/category_of_latrine',
	'choose_type_septic':'sanitation_group/septic_group/septic',
	'category_of_septic':'sanitation_group/septic_group/category_of_septic',
	'septic_tank_system_accessibility':'sanitation_group/septic_group/septic_accessible',
	'choose_sewer_type':'sanitation_group/sewer',
	'overall_service':'sanitation_group/satisfaction_group/scale/overall_service',
	'hours_of_supply_per_day':'sanitation_group/satisfaction_group/scale/hours_per_day',
	'water_quality':'sanitation_group/satisfaction_group/scale/water_quality',
	'water_pressure':'sanitation_group/satisfaction_group/scale/water_pressure',
	'cost_of_water':'sanitation_group/satisfaction_group/scale/cost_of_water',
	'bills':'sanitation_group/satisfaction_group/scale/bills',
	'repairs':'sanitation_group/satisfaction_group/scale/repairs',
	'response_to_filed_complaints':'sanitation_group/satisfaction_group/scale/communication',
	'reported_leakages':'sanitation_group/satisfaction_group/scale/reported_leakages',
	'gps_cordinates':'gps_location',
	'remarks':'remarks',
}

@frappe.whitelist()
def fetch_cis_from_ona():
	'''
	Function that fetches CIS entries from ONA online
	this is the main function for pulling cis entries 
	which calls all the other methods
	NB: it can be run both manually or using a cronjob 
	under scheduler events in the hooks.py for water app 
	app
	'''
	# check if fetching data is on
	cis_settings = frappe.get_single("CIS Settings")
	current_cis_project = cis_settings.fetching_cis_data_on
	if current_cis_project:
		# check if cis table is defined
		if cis_settings.ona_table_cis:
			table_id = cis_settings.ona_table_cis
		else:
			# create an error record in Washmis Error Log list
			undefined_table_error_msg = "The Ona CIS table to pull data from is not defined in CIS Settings"
			# save error
			save_washmis_error_log("Undefined Table Name",undefined_table_error_msg)
			return {'status':False,'message':undefined_table_error_msg}

		# check if last fetch date defined
		if cis_settings.date_of_last_fetched_cis:
			date_of_last_fetched_cis = cis_settings.date_of_last_fetched_cis
		else:
			date_of_last_fetched_cis = datetime.datetime(1970,1,1)

		# check if a request zone is defined
		if cis_settings.water_utility:
			zone_or_utility_name = cis_settings.water_utility
		else:
			# create an error record in Washmis Error Log list
			error_msg = "Water Utility/Operator to pull data for is not defined in CIS Settings"
			# save error
			save_washmis_error_log("Undefined Utility/Operator",error_msg)
			return {'status':False,'message':error_msg}			
		
		# defined other parameters for Ona.io
		ona_url = 'https://api.ona.io/api/v1/data/'
		auth_set = ('upande','upandegani')
		# call the fetch function
		response = fetch_cis_from_ona_table(table_id,date_of_last_fetched_cis,ona_url,auth_set,zone_or_utility_name)
		reponse_in_json = response.json()
		# loop through cis entries
		for cis_entry in response.json():
			# save the cis entries
			try:
				save_to_cis_data(cis_entry,list_of_ona_fields_to_cis_data)
				# save the date of the last _submission_time
				if reponse_in_json.index(cis_entry)+1 == len(reponse_in_json):
					doc = frappe.get_doc("CIS Settings")
					doc.date_of_last_fetched_cis = cis_entry['_submission_time']
					doc.save()
					frappe.db.commit()
			except:
				error_msg = "Error occured saving entries please check CIS Settings"
				# save error
				save_washmis_error_log("Saving CIS Entries Failed",error_msg)
				return {'status':False,'message':'Saving CIS Entries Failed'}
	# finally return true when fetching is complete
	return {'status':True}

def fetch_cis_from_ona_table(table_id,date_of_last_fetched_cis,ona_url,auth_set,zone):
    '''
    Function that fetches data from a given Ona.io table whose submission date is 
    i.e _submission_time is greater or equal to the given datetime i.e 
    date_of_last_fetched_cis
    input:
        table_id - int
        date_of_last_fetched_cis - datetime object
        ona_url - str
        auth_set - set
    output
        response - object(with all the new entries)
    '''
    # serialize the datetime object i.e date_of_last_fetched_cis to string
    if type(date_of_last_fetched_cis) == str:
        last_datetime_serialized = date_of_last_fetched_cis
    else:
        last_datetime_serialized = json_serial(date_of_last_fetched_cis)
    # construct the query sting
    query_str ={"_submission_time":{"$gte":last_datetime_serialized},'service_area_details/zone':zone}
    # construct the request url with the correct parameters
    request_url = ona_url+str(table_id)+'?query='+json.dumps(query_str)
    # send API get request with the constructed request_url
    response = requests.get(
        request_url,
        auth=auth_set
    )
    return response

def capitalize_n_translate(name):
	'''
	Function that calls the two functions
	in order to capitalize and translate a
	name based on the given language
	'''
	# capitalized name
	capitalized_name = capitalize_name_separeted_by_underscores(name)
	# translated name
	tranlated_name = convert_ona_options_to_system_language(capitalized_name)
	# return the final name
	return tranlated_name

def convert_ona_options_to_system_language(name):
	'''
	Function that converts any option from ONA that
	is in English to language given by the system
	with the help of available translations
	input:
		name (in english)
	output:
		name in system language e.g portugese
	'''
	# get the Washmis ERP global language
	washmis_global_settings = frappe.get_single("CIS Settings")
	language = washmis_global_settings.language
	if language == "en":
		# return the defualt i.e still in english
		return name
	else:
		# get the correct translation in the new language
		list_of_translation = frappe.get_list("Translation",
			fields=["target_name"],
			filters = {
				"language":language,
				"source_name":name
		})
		# check if any is found
		if len(list_of_translation) > 0:
			# return the language tranlation
			return list_of_translation[0]['target_name']
		else:
			# return initial name if not translation is available
			return name

def capitalize_name_separeted_by_underscores(name):
	'''
	Function that converts a string given in this format
	"text_text" to "Text Text"
	input:
		name - str
	output:
		capitalized name
	'''
	return reduce(lambda a,b: a+" "+b,list(map(lambda x :x.capitalize(),str(name).split("_"))))

def save_to_cis_data(cis_entry,list_of_ona_fields_to_cis_data):
	'''
	Function that saves a given cis entry to the
	CIS Data doctype list after checking if its 
	already saved or not
	input:
		cis_entry
	output:
		boolean True/False
	'''
	# check if the cis entry is already saved
	cis_with_id_list = frappe.get_list("CIS Data", filters={'_id':cis_entry['_id']})
	if len(cis_with_id_list) > 0:
		# record is already saved
		pass
	else:
		list_of_all_fields = []
		key_n_values_for_entry = {}
		for field_key in list_of_ona_fields_to_cis_data:
			try:
				if cis_entry[list_of_ona_fields_to_cis_data[field_key]]:
					list_of_all_fields.append(list_of_ona_fields_to_cis_data[field_key])
					key_n_values_for_entry[field_key] = cis_entry[list_of_ona_fields_to_cis_data[field_key]]
			except:
				# if no value exists set it to empty since all fields are data fields
				key_n_values_for_entry[field_key] = ""

		# save the cis record for data
		doc = frappe.new_doc("CIS Data")
		doc._id = key_n_values_for_entry['_id']
		doc.collector_name = capitalize_n_translate(key_n_values_for_entry['collector_name'])
		doc.date = capitalize_n_translate(key_n_values_for_entry['date'])
		doc.zone = capitalize_n_translate(key_n_values_for_entry['zone'])
		doc.sub_zone = capitalize_n_translate(key_n_values_for_entry['sub_zone'])
		doc.type_of_housing = capitalize_n_translate(key_n_values_for_entry['type_of_housing'])
		doc.type_of_premises = capitalize_n_translate(key_n_values_for_entry['type_of_premises'])
		doc.type_of_residential_or_mixed_premise = capitalize_n_translate(key_n_values_for_entry['type_of_residential_or_mixed_premise'])
		doc.number_of_people_in_the_household = capitalize_n_translate(key_n_values_for_entry['number_of_people_in_the_household'])
		doc.type_of_commercial_premise = capitalize_n_translate(key_n_values_for_entry['type_of_commercial_premise'])
		doc.type_of_institution = capitalize_n_translate(key_n_values_for_entry['type_of_institution'])
		doc.type_of_health_facility = capitalize_n_translate(key_n_values_for_entry['type_of_health_facility'])
		doc.category_of_health_facility = capitalize_n_translate(key_n_values_for_entry['category_of_health_facility'])
		doc.category_of_institution = capitalize_n_translate(key_n_values_for_entry['category_of_institution'])
		doc.number_of_people_in_institution = capitalize_n_translate(key_n_values_for_entry['number_of_people_in_institution'])
		doc.email_of_the_institution = capitalize_n_translate(key_n_values_for_entry['email_of_the_institution'])
		doc.average_number_of_people_served_at_the_fontenerio_per_day = capitalize_n_translate(key_n_values_for_entry['average_number_of_people_served_at_the_fontenerio_per_day'])
		doc.first_name_landlord = capitalize_n_translate(key_n_values_for_entry['first_name_landlord'])
		doc.land_lord_or_owner_surname = capitalize_n_translate(key_n_values_for_entry['land_lord_or_owner_surname'])
		doc.land_lord_or_owner_cell = capitalize_n_translate(key_n_values_for_entry['land_lord_or_owner_cell'])
		doc.customer_details_same_as_landlord = capitalize_n_translate(key_n_values_for_entry['customer_details_same_as_landlord'])
		doc.different_customer_name = capitalize_n_translate(key_n_values_for_entry['different_customer_name'])
		doc.different_customer_cell = capitalize_n_translate(key_n_values_for_entry['different_customer_cell'])
		doc.does_customer_have_a_connection = capitalize_n_translate(key_n_values_for_entry['does_customer_have_a_connection'])
		doc.customer_have_a_connection = capitalize_n_translate(key_n_values_for_entry['customer_have_a_connection'])
		doc.account_no = capitalize_n_translate(key_n_values_for_entry['account_no'])
		doc.account_name = capitalize_n_translate(key_n_values_for_entry['account_name'])
		doc.total_number_of__households_in_the_mdu = capitalize_n_translate(key_n_values_for_entry['total_number_of__households_in_the_mdu'])
		doc.average_number_of_people_in_each_household_ = capitalize_n_translate(key_n_values_for_entry['average_number_of_people_in_each_household_'])
		doc.billing_status = capitalize_n_translate(key_n_values_for_entry['billing_status'])
		doc.why_customer_is_not_billed = capitalize_n_translate(key_n_values_for_entry['why_customer_is_not_billed'])
		doc.frequency_of_bill_delivery = capitalize_n_translate(key_n_values_for_entry['frequency_of_bill_delivery'])
		doc.connection_status = capitalize_n_translate(key_n_values_for_entry['connection_status'])
		doc.how_often_do_you_receive_water = capitalize_n_translate(key_n_values_for_entry['how_often_do_you_receive_water'])
		doc.days_with_supply = capitalize_n_translate(key_n_values_for_entry['days_with_supply'])
		doc.daily_hours = capitalize_n_translate(key_n_values_for_entry['daily_hours'])
		doc.hours_with_supply_daily = capitalize_n_translate(key_n_values_for_entry['hours_with_supply_daily'])
		doc.last_time_to_receive_water = capitalize_n_translate(key_n_values_for_entry['last_time_to_receive_water'])
		doc.storage_tank_available = capitalize_n_translate(key_n_values_for_entry['storage_tank_available'])
		doc.storage_tank_location = capitalize_n_translate(key_n_values_for_entry['storage_tank_location'])
		doc.storage_tank_size = capitalize_n_translate(key_n_values_for_entry['storage_tank_size'])
		doc.disconnection_duration = capitalize_n_translate(key_n_values_for_entry['disconnection_duration'])
		doc.water_sources = capitalize_n_translate(key_n_values_for_entry['water_sources'])
		doc.name_of_sssp = capitalize_n_translate(key_n_values_for_entry['name_of_sssp'])
		doc.name_community_project_ = capitalize_n_translate(key_n_values_for_entry['name_community_project_'])
		doc.water_connection = capitalize_n_translate(key_n_values_for_entry['water_connection'])
		doc.meter_location = capitalize_n_translate(key_n_values_for_entry['meter_location'])
		doc.why_access_to_meter_location_is_denied = capitalize_n_translate(key_n_values_for_entry['why_access_to_meter_location_is_denied'])
		doc.meter_status = capitalize_n_translate(key_n_values_for_entry['meter_status'])
		doc.meter_settlement = capitalize_n_translate(key_n_values_for_entry['meter_settlement'])
		doc.meter_material = capitalize_n_translate(key_n_values_for_entry['meter_material'])
		doc.inlet_pipe_size = capitalize_n_translate(key_n_values_for_entry['inlet_pipe_size'])
		doc.meter_size = capitalize_n_translate(key_n_values_for_entry['meter_size'])
		doc.meter_position = capitalize_n_translate(key_n_values_for_entry['meter_position'])
		doc.meter_flow_direction = capitalize_n_translate(key_n_values_for_entry['meter_flow_direction'])
		doc.item = capitalize_n_translate(key_n_values_for_entry['item'])
		doc.valve_before_meter = capitalize_n_translate(key_n_values_for_entry['valve_before_meter'])
		doc.valve_after_meter = capitalize_n_translate(key_n_values_for_entry['valve_after_meter'])
		doc.meter_seal = capitalize_n_translate(key_n_values_for_entry['meter_seal'])
		doc.connection_seal = capitalize_n_translate(key_n_values_for_entry['connection_seal'])
		doc.meter_liners = capitalize_n_translate(key_n_values_for_entry['meter_liners'])
		doc.pipe_material = capitalize_n_translate(key_n_values_for_entry['pipe_material'])
		doc.state_of_the_meter = capitalize_n_translate(key_n_values_for_entry['state_of_the_meter'])
		doc.meter_brand = capitalize_n_translate(key_n_values_for_entry['meter_brand'])
		doc.meter_serial_no = capitalize_n_translate(key_n_values_for_entry['meter_serial_no'])
		doc.meter_class = capitalize_n_translate(key_n_values_for_entry['meter_class'])
		doc.readings_of_the_meter = capitalize_n_translate(key_n_values_for_entry['readings_of_the_meter'])
		doc.metering_problems = capitalize_n_translate(key_n_values_for_entry['metering_problems'])
		doc.meter_read_monthly = capitalize_n_translate(key_n_values_for_entry['meter_read_monthly'])
		doc.installation_date_known = capitalize_n_translate(key_n_values_for_entry['installation_date_known'])
		doc.tentative_year_of_installation = capitalize_n_translate(key_n_values_for_entry['tentative_year_of_installation'])
		doc.installation_date = capitalize_n_translate(key_n_values_for_entry['installation_date'])
		doc.customer_willing_to_be_connected = capitalize_n_translate(key_n_values_for_entry['customer_willing_to_be_connected'])
		doc.approximate_distance = capitalize_n_translate(key_n_values_for_entry['approximate_distance'])
		doc.number_of_people_in_multi_dwelling_household = capitalize_n_translate(key_n_values_for_entry['number_of_people_in_multi_dwelling_household'])
		doc.average_number_of_people_in_each_household = capitalize_n_translate(key_n_values_for_entry['average_number_of_people_in_each_household'])
		doc.water_source = capitalize_n_translate(key_n_values_for_entry['water_source'])
		doc.name_of_sssp_ = capitalize_n_translate(key_n_values_for_entry['name_of_sssp_'])
		doc.name_community_project = capitalize_n_translate(key_n_values_for_entry['name_community_project'])
		doc.type_of_sanitation = capitalize_n_translate(key_n_values_for_entry['type_of_sanitation'])
		doc.onsite_category = capitalize_n_translate(key_n_values_for_entry['onsite_category'])
		doc.choose_type_of_pit_latrine = capitalize_n_translate(key_n_values_for_entry['choose_type_of_pit_latrine'])
		doc.category_type_of_pit_latrine = capitalize_n_translate(key_n_values_for_entry['category_type_of_pit_latrine'])
		doc.choose_type_septic = capitalize_n_translate(key_n_values_for_entry['choose_type_septic'])
		doc.category_of_septic = capitalize_n_translate(key_n_values_for_entry['category_of_septic'])
		doc.septic_tank_system_accessibility = capitalize_n_translate(key_n_values_for_entry['septic_tank_system_accessibility'])
		doc.choose_sewer_type = capitalize_n_translate(key_n_values_for_entry['choose_sewer_type'])
		doc.overall_service = capitalize_n_translate(key_n_values_for_entry['overall_service'])
		doc.hours_of_supply_per_day = capitalize_n_translate(key_n_values_for_entry['hours_of_supply_per_day'])
		doc.water_quality = capitalize_n_translate(key_n_values_for_entry['water_quality'])
		doc.water_pressure = capitalize_n_translate(key_n_values_for_entry['water_pressure'])
		doc.cost_of_water = capitalize_n_translate(key_n_values_for_entry['cost_of_water'])
		doc.bill = capitalize_n_translate(key_n_values_for_entry['bills'])
		doc.repairs = capitalize_n_translate(key_n_values_for_entry['repairs'])
		doc.response_to_filed_complaints = capitalize_n_translate(key_n_values_for_entry['response_to_filed_complaints'])
		doc.reported_leakages = capitalize_n_translate(key_n_values_for_entry['reported_leakages'])
		doc.gps_cordinates = capitalize_n_translate(key_n_values_for_entry['gps_cordinates'])
		doc.remarks = capitalize_n_translate(key_n_values_for_entry['remarks'])
		# now save the document
		doc.save()
		frappe.db.commit()
	
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


def save_washmis_error_log(title,message):
	'''
	Function that save an error to the washmis 
	ERP errot log list
	'''
	doc = frappe.new_doc("System Error Log")
	doc.title = title
	doc.error = message
	doc.save()
	frappe.db.commit()