# frappe imports
import frappe
from .dynamic_dashboard_settings import determine_setting

@frappe.whitelist(allow_guest = True)
def get_cis_data():
    '''
    Function that pulls all cis data from the database
    input:
        None
    output
        list of cis entries in the database
    '''
    list_of_cis_data = frappe.get_list("CIS Data", 
        fields=['*'],
        filters = {}
        )
    # now return the cis data
    return list_of_cis_data

@frappe.whitelist(allow_guest = True)
def filter_cis_data_for_chart():
    '''
    Function that is used to filter the collected cis 
    data to get appropriate dashboard data
    input:
        currently none
    output
        not yet defined
    '''
    if 'System Manager' in frappe.get_roles(frappe.session.user):
        pass
    else:
        return {
            'status':False,
            'message':'You don\'t have sufficient permissions to view this page'
        }
    # get current system language
    cis_settings = frappe.get_single("CIS Settings")
    language = cis_settings.language
    # check if global language is defined
    if language:
        pass
    else:
        return {'status':False,
            'message':'Language not set in CIS Settings'
        }
    # check if tranlations for that language is defined
    determined_settings = determine_setting(language)
    if determined_settings['status']:
        required_dashboard_based_on_settings = determined_settings['settings']
    else:
        return {'status':False,
            'message':'Chart Setting for {} are not set'.format(language)
        }

    # initialize values and amounts as an empty dictionary
    values_n_amounts = {}
    # get all cis data
    list_of_cis_data = get_cis_data()
    # loop through the found cis data
    for cis_data in list_of_cis_data:
        # loop through the dashbaords and create the required values
        for required_cis_dashboard in required_dashboard_based_on_settings:
            dashboard_title = required_cis_dashboard['dashboard_title']  
            other_fields_to_check = required_cis_dashboard['other_fields_to_check']
            other_required_fields = True #initialize it to True
            # check that all the other required fields have been filled
            if len(other_fields_to_check) > 0:
                # other fields to check exist
                for other_field_to_check in other_fields_to_check:
                    required_field = other_field_to_check['field_name']
                    required_value = other_field_to_check['required_value']                    
                    # check if the value of the field is the required one
                    if str.lower(cis_data[required_field]) == str.lower(required_value):
                        pass
                    else:
                        other_required_fields = False
                        # break since there is no need to continue as some requirements are not met
                        break

            # frappe.throw("pause")
            # if some fields are not met just pass do not add this record
            if not other_required_fields:
                pass
            else:
                # continue to get values from field_to_check
                # check if dashboard title is already added to values_n_amounts
                if dashboard_title in values_n_amounts.keys():
                    pass
                else:
                    # add the title to values_n_amounts
                    values_n_amounts[dashboard_title] = {
                        'chart_settings':{
                            'chart_id':required_cis_dashboard['chart_id'],
                            'chart_type':required_cis_dashboard['chart_type']
                        }
                    }

                # check if the value holders have been added
                current_cis_value = cis_data[required_cis_dashboard['field_to_check']]
                if current_cis_value:
                    # check if the required dashboard is a multiple dataset
                    if required_cis_dashboard['data_fomart'] == "multiple_dataset":
                        secondary_cis_value = cis_data[required_cis_dashboard['secondary_field']]
                        # if the secondary field value is defined
                        if secondary_cis_value:
                            if str.capitalize(current_cis_value) in values_n_amounts[dashboard_title].keys():
                                # now check if the secondary key value has been added
                                if str.capitalize(secondary_cis_value) in values_n_amounts[dashboard_title][str.capitalize(current_cis_value)].keys():
                                    values_n_amounts[dashboard_title][str.capitalize(current_cis_value)][str.capitalize(secondary_cis_value)] += 1
                                else:
                                    values_n_amounts[dashboard_title][str.capitalize(current_cis_value)][str.capitalize(secondary_cis_value)] = 1
                            else:
                                # add to the value to values_n_amounts
                                values_n_amounts[dashboard_title][str.capitalize(current_cis_value)] = {}
                                values_n_amounts[dashboard_title][str.capitalize(current_cis_value)][str.capitalize(secondary_cis_value)] = 1

                    else:
                        if str.capitalize(current_cis_value) in values_n_amounts[dashboard_title].keys():
                            # add to the amount
                            values_n_amounts[dashboard_title][str.capitalize(current_cis_value)] += 1
                        else:
                            # add the value to values_n_amounts
                            values_n_amounts[dashboard_title][str.capitalize(current_cis_value)] = 1
    # check if any data was found
    if len(values_n_amounts.keys()) > 0:
        values_n_amounts['status'] = True
        values_n_amounts['message'] = ''
        # Customer Satisfaction Dashboard
        values_n_amounts['Customer Satisfaction'] = customer_satisfaction_function(list_of_cis_data)
    else:
        values_n_amounts['status'] = False
        values_n_amounts['message'] = 'No CIS data found'
    # add the language
    values_n_amounts['language'] = language
    # now return the results
    return values_n_amounts

def customer_satisfaction_function(list_of_cis_data):
    fields_to_check = {
        'Overall Service':{'field_name':'overall_service','amount_value':0,'counter':0},
        'Hours of Supply per Day':{'field_name':'hours_of_supply_per_day','amount_value':0,'counter':0},
        'Water Quality/ Colour':{'field_name':'water_quality','amount_value':0,'counter':0},
        'Water Pressure':{'field_name':'water_pressure','amount_value':0,'counter':0},
        'Cost of Water':{'field_name':'cost_of_water','amount_value':0,'counter':0},
        'Bills':{'field_name':'bill','amount_value':0,'counter':0},
        'Quality of Repairs':{'field_name':'repairs','amount_value':0,'counter':0},
        'Response to Filed Complaints':{'field_name':'response_to_filed_complaints','amount_value':0,'counter':0},
        'Response to Reported Leakages':{'field_name':'reported_leakages','amount_value':0,'counter':0}
    }
        
    # loop through cis data
    for cis_data in list_of_cis_data:
        # loop through fields to check
        for field_to_check in fields_to_check.keys():
            current_field_to_check_dict = fields_to_check[field_to_check]
            # check if the value exist
            current_cis_value = cis_data[current_field_to_check_dict['field_name']]
            if current_cis_value:
                # add to amount and counter
                fields_to_check[field_to_check]['amount_value'] += int(current_cis_value)
                fields_to_check[field_to_check]['counter'] += 1
        
    # once the loop is complete generated averages and create a dataset
    current_values_n_amounts = {'chart_settings':{
        'chart_id':'customer_satisfaction',
        'chart_type':'bar'
        }
    }
    for k,v in fields_to_check.items():
        try:
            current_avarage = round(v['amount_value']/v['counter'],2)
        except:
            current_avarage = 0
        current_values_n_amounts[k] = current_avarage

    # return current values and amounts
    return current_values_n_amounts