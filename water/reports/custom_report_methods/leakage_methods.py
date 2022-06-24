from __future__ import unicode_literals
from functools import reduce 

# std lib imports
import requests,json,datetime,json,datetime
import frappe

list_of_ona_fields_to_leakage_data = {
	'id':'_id',
	'submission_date':'_submission_time',
	'geolocation_data':'Record_your_current_location',
	'Description':'description',
	'utility':'utility'
}

@frappe.whitelist()
def fetch_leakage_from_ona():
	'''
	Function that fetches leakage entries from ONA online
	this is the main function for pulling leakage entries 
	which calls all the other methods
	NB: it can be run both manually or using a cronjob 
	under scheduler events in the hooks.py for water app 
	'''
    #get report settings
	report_settings = frappe.get_single("Report Settings")
	# check if fetching data is on
	if report_settings.fetch_leakage:
		# check if leakage table is defined
		if report_settings.ona_table:
			table_id = report_settings.ona_table
		else:
			# create an error record in System Error Log list
			undefined_table_error_msg = "The Ona Leakage table to pull data from is not defined in Report Settings"
			# save error
			save_system_error_log("Undefined Table Name",undefined_table_error_msg)
			return {'status':False,'message':undefined_table_error_msg}

		# check if last fetch date defined
		if report_settings.leakage_data_last_fetch:
			leakage_data_last_fetch = report_settings.leakage_data_last_fetch
		else:
			leakage_data_last_fetch = datetime.datetime(1970,1,1)

		# check if a request zone is defined
		if report_settings.utility_name:
			utility_name = report_settings.utility_name
		else:
			# create an error record in System Error Log list
			error_msg = "Water Utility/Operator to pull data for is not defined in Report Settings for Leakage"
			# save error
			save_system_error_log("Undefined Utility/Operator",error_msg)
			return {'status':False,'message':error_msg}			
		
		# defined other parameters for Ona.io
		ona_url = 'https://api.ona.io/api/v1/data/'
		auth_set = ('upande','upandegani')
		# call the fetch function
		response = fetch_leakage_data_from_ona_table(table_id,leakage_data_last_fetch,ona_url,auth_set,utility_name)
		reponse_in_json = response.json()
		# loop through cis entries
		for leakage_entry in response.json():
			# save the leakage entries
			try:
				save_to_leakage_data(leakage_entry,list_of_ona_fields_to_leakage_data)
				# save the date of the last _submission_time
				if reponse_in_json.index(leakage_entry)+1 == len(reponse_in_json):
					doc = frappe.get_doc("Report Settings")
					doc.leakage_data_last_fetch = leakage_entry['_submission_time']
					doc.save()
					frappe.db.commit()
			except:
				error_msg = "Error occured saving entries please check Report Settings"
				# save error
				save_system_error_log("Saving Report Entries Failed",error_msg)
				return {'status':False,'message':'Saving Report Entries Failed'}
	# finally return true when fetching is complete
	return {'status':True}

def fetch_leakage_data_from_ona_table(table_id,leakage_data_last_fetch,ona_url,auth_set,utility_name):
    '''
    Function that fetches data from a given Ona.io table whose submission date is 
    i.e _submission_time is greater or equal to the given datetime i.e 
    date_of_last_fetched_cis
    input:
        table_id - int
        leakage_data_last_fetch - datetime object
        ona_url - str
        auth_set - set
		utility_name - str
    output
        response - object(with all the new entries)
    '''
    # serialize the datetime object i.e date_of_last_fetched_cis to string
    if type(leakage_data_last_fetch) == str:
        last_datetime_serialized = leakage_data_last_fetch
    else:
        last_datetime_serialized = json_serial(leakage_data_last_fetch)
    # construct the query sting
    query_str ={"_submission_time":{"$gte":last_datetime_serialized},'utility':utility_name}
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
	washmis_global_settings = frappe.get_single("Report Settings")
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

def save_to_leakage_data(leakage_entry,list_of_ona_fields_to_leakage_data):
	'''
	Function that saves a given leakage entry to the
	Leakage Data doctype list after checking if its 
	already saved or not
	input:
		leakage_entry
	output:
		boolean True/False
	'''
	# check if the leakage_entry entry is already saved
	leakage_with_id_list = frappe.get_list("Leakage",filters={'id':leakage_entry['_id']})
	if len(leakage_with_id_list) > 0:
		# record is already saved
		pass
	else:
		list_of_all_fields = []
		key_n_values_for_entry = {}
		for field_key in list_of_ona_fields_to_leakage_data:
			try:
				if leakage_entry[list_of_ona_fields_to_leakage_data[field_key]]:
					list_of_all_fields.append(list_of_ona_fields_to_leakage_data[field_key])
					key_n_values_for_entry[field_key] = leakage_entry[list_of_ona_fields_to_leakage_data[field_key]]
			except:
				# if no value exists set it to empty since all fields are data fields
				key_n_values_for_entry[field_key] = ""

		# save the cis record for data
		doc = frappe.new_doc("Leakage")
		doc.id = key_n_values_for_entry['id']
		doc.submission_date = key_n_values_for_entry['submission_date']
		doc.geolocation_data = capitalize_n_translate(key_n_values_for_entry['geolocation_data'])
		doc.description = capitalize_n_translate(key_n_values_for_entry['Description'])
		doc.utility = capitalize_n_translate(key_n_values_for_entry['utility'])
		
		# now save the document
		doc.save(ignore_permissions = True)
		frappe.db.commit()
	
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


def save_system_error_log(title,message):
	'''
	Function that save an error to the washmis 
	ERP errot log list
	'''
	doc = frappe.new_doc("System Error Log")
	doc.title = title
	doc.error = message
	doc.save()
	frappe.db.commit()