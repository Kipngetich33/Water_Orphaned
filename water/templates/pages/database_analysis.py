# frappe imports
import frappe

# required_cis_dashboards1 = [
#     {'dashboard_title':'Customer Satisfaction',
#         'custom_function':True,
#         'function_name':test_function,
#         # 'field_to_check':'type_of_residential_or_mixed_premise',
#         'data_fomart':'single_dataset',
#         # 'other_fields_to_check':[],
#         'chart_id':'customer_satisfaction',
#         'chart_type':'bar'
#     },
# ]

# global variables
required_cis_dashboards = [{'dashboard_title':'Customer Connected to WSP',
        'field_to_check':'does_customer_have_a_connection',
        'data_fomart':'single_dataset',
        'other_fields_to_check':[],
        'chart_id':'customer_connected_to_wsp',
        'chart_type':'pie'
    },
    {'dashboard_title':'Account Details Known',
        'field_to_check':'customer_have_a_connection',
        'data_fomart':'single_dataset',
        'other_fields_to_check':[{'field_name':'does_customer_have_a_connection',
           'required_value':'Yes'
        }],
        'chart_id':'account_details_known',
        'chart_type':'doughnut'
    },
]

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
def get_billing_dabase_details_data():
    '''
    Function that pulls all Billing Database Detail data 
    from the databa
    input:
        None
    output
        list of Billing Database Detail in the database
    '''
    list_billing_database_details = frappe.get_list("Billing Database Detail", 
        fields=['*'],
        filters = {}
        )
    # now return the cis data
    return list_billing_database_details


@frappe.whitelist(allow_guest = True)
def filter_cis_data_for_chart():
    '''
    Function that is used to filter the collected cis 
    data to get appropriate dashboard data
    input:
        currently none
    output:
        dictionary of values and amounts
    '''
    values_n_amounts = {}
    # get all cis data
    list_of_cis_data = get_cis_data()
    
    for cis_data in list_of_cis_data:
        # loop through the dashbaords and create the required values
        for required_cis_dashboard in required_cis_dashboards:
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
    
    # adding the database reconcilliation data to the values_n_amounts
    database_reconciliation_data = cis_database_comparison(list_of_cis_data)
    for database_analyis_key,database_analyis_value in database_reconciliation_data.items():
        values_n_amounts[database_analyis_value['title']] = {
            'No':database_analyis_value['no'],
            'Yes':database_analyis_value['yes'],
            'chart_settings':{
                'chart_id':database_analyis_key,
                'chart_type':'pie',
                'chart_status':database_analyis_value['chart_status']
            }
        }

    # now return the results
    return values_n_amounts


def cis_database_comparison(list_of_cis_data):
    '''
    Function that loops through given cis data and
    compares it to data in the database
    '''
    reconciliation_data = {
        'potentials_with_number_in_database':{
            'title':'Customers who said they have no connection but their phone number is in the database',
            'yes':0,
            'no':0,
            'chart_status':True
        },
        'matched_phone_numbers':{
            'title':'Customer Phone Numbers From CIS Matching those in the Billing Database',
            'yes':0,
            'no':0,
            'chart_status':True
        },
        'phone_number_not_in_database_but_in_cis':{
            'title':'Phone Number not in the Billing Database but Provided in CIS',
            'yes':0,
            'no':0,
            'chart_status':True
        },
        'phone_number_not_in_database_or_cis':{
            'title':'No Phone Number in the Billing Database and Not Provided During CIS',
            'yes':0,
            'no':0,
            'chart_status':False
        },
        'matched_account_numbers':{
            'title':'Account Numbers in CIS Matching those in the Billing Database',
            'yes':0,
            'no':0,
            'chart_status':True
        },
        'matched_account_names':{
            'title':'Account Number in CIS belongs to a different Account Name in Database',
            'yes':0,
            'no':0,
            'chart_status':True
        },
        'issued_wrong_account_number':{
            'title':'Issued Wrong Account Number',
            'yes':0,
            'no':0,
            'chart_status':True
        },
        'no_account_details_given':{
            'title':'No Account Details Provided',
            'yes':0,
            'no':0,
            'chart_status':True
        }
    }
    # loop through the cis data
    for cis_data in list_of_cis_data:
        # check if customer has a connection
        if cis_data.does_customer_have_a_connection == "yes":
            # check if account number is given
            if cis_data.account_no and \
            cis_data.account_no != '0' and \
            cis_data.account_no != 'O':
                # some account details are given hence # 9.No account details provided
                reconciliation_data['no_account_details_given']['no'] += 1
                # filter billing database detail by account number
                found_result = get_filtered_result({'account_no':cis_data.account_no})
                #1. check if account number in cis match those in database
                if found_result['status']:
                    # a match was found
                    reconciliation_data['matched_account_numbers']['yes'] += 1
                    # correct account number issued
                    reconciliation_data['issued_wrong_account_number']['no'] += 1
                    # get phone number from cis
                    if cis_data.customer_details_same_as_landlord == "yes":
                        customer_phone_number = cis_data.land_lord_or_owner_cell
                    else:
                        customer_phone_number = cis_data.different_customer_cell
                    # 2. check phone number match that in database
                    try:
                        # check if customer_phone_number  is defined
                        if customer_phone_number and int(customer_phone_number) != 0:
                            pass
                            # check if number match that in database 
                            try:
                                if int(customer_phone_number) == int(found_result['value'].customer_tel_number):
                                    reconciliation_data['matched_phone_numbers']['yes'] += 1
                                else:
                                    reconciliation_data['matched_phone_numbers']['no'] += 1
                            except:
                                pass
                    except:
                        pass

                    # 4. No Phone number provided in database but provided in CIS
                    try:
                        # check if customer_phone_number  is defined
                         if customer_phone_number and int(customer_phone_number) != 0:
                            # check if number in database
                            try:
                                if found_result['value'].customer_tel_number and \
                                int(found_result['value'].customer_tel_number)!= 0:
                                    reconciliation_data['phone_number_not_in_database_but_in_cis']['no'] += 1
                                else:
                                    reconciliation_data['phone_number_not_in_database_but_in_cis']['yes'] += 1
                            except:
                                pass
                    except:
                        pass

                    # 5. No phone number in database and not provided in CIS
                    # phone_number_not_in_database_or_cis
                    try:
                        # check if customer_phone_number is not defined
                        if not customer_phone_number or int(customer_phone_number) == 0:
                            # check if number not in database
                            try:
                                if found_result['value'].customer_tel_number and \
                                int(found_result['value'].customer_tel_number)!= 0:
                                    reconciliation_data['phone_number_not_in_database_or_cis']['no'] += 1
                                else:
                                    reconciliation_data['phone_number_not_in_database_or_cis']['yes'] += 1
                            except:
                                pass
                        else:
                            reconciliation_data['phone_number_not_in_database_or_cis']['no'] += 1
                    except:
                        pass

                    # 6. Account Number belongs to a different account name
                    # check if account names match
                    try:
                        # get account name in cis
                        account_name_in_cis = cis_data.account_name
                        # check if name is defined
                        if len(account_name_in_cis) != 0:
                            # check if the name matches that in the database
                            if account_name_in_cis == found_result['value'].account_name:
                                reconciliation_data['matched_account_names']['no'] += 1
                            else:
                                reconciliation_data['matched_account_names']['yes'] += 1
                        else:
                            # pass because account name is not defined
                            pass
                    except:
                        pass

                    # 8. Issued Wrong Account Number
                    try:
                        # check if customer account name matches
                        if not customer_phone_number or int(customer_phone_number) == 0:
                            # check if number not in database
                            try:
                                if found_result['value'].customer_tel_number and \
                                int(found_result['value'].customer_tel_number)!= 0:
                                    pass
                                else:
                                    reconciliation_data['phone_number_not_in_database_or_cis']['yes'] += 1
                            except:
                                pass
                    except:
                        pass

                    
                else:
                    # did not match
                    reconciliation_data['matched_account_numbers']['no'] += 1
                    # wrong account number issued
                    reconciliation_data['issued_wrong_account_number']['yes'] += 1
            else:
                # 9.No account details provided
                # check id account name is given
                if cis_data.account_name and cis_data.account_name != "" and \
                cis_data.account_name != 0 and cis_data.account_name != '0':
                    reconciliation_data['no_account_details_given']['no'] += 1
                else:
                    reconciliation_data['no_account_details_given']['yes'] += 1

        else:
            # check for potentials with number in database
            if cis_data.customer_details_same_as_landlord == "yes":
                cell_number = cis_data.land_lord_or_owner_cell
            else:
                cell_number = cis_data.different_customer_cell
            try:
                # check if cell number is defined
                if cell_number and int(cell_number) != 0:
                    # check if number is already in database
                    list_of_phone_cis_data = frappe.get_list("Billing Database Detail", 
                        fields=['*'],
                        filters = {'customer_tel_number':cell_number}
                    )
                    if len(list_of_phone_cis_data)>0:
                        # number exists in database
                        reconciliation_data['potentials_with_number_in_database']['yes'] += 1
                    else:
                        # number not in database
                        reconciliation_data['potentials_with_number_in_database']['no'] += 1
            except:
                pass

    return reconciliation_data

def get_filtered_result(required_filter):
    filter_value = list(required_filter.values())[0]
    alternate_filter_value = {'status':False}
    try:
        if type(filter_value) == str:
            alternate_filter_value = {'status':True,'value':int(filter_value)}
        elif type(filter_value) == int:
            alternate_filter_value = {'status':True,'value':str(filter_value)}
    except:
        pass
    
    # check filter value from database with original filter
    list_of_billing_database_data = frappe.get_list("Billing Database Detail", 
        fields=['*'],
        filters = required_filter
    )
    
    # check what you need to return
    if len(list_of_billing_database_data) > 0:
        return {'status':True,'value':list_of_billing_database_data[0]}
    else:
        try:
            # try alternative value
            if alternate_filter_value['status']:
                list_of_alt_billing_database_data = frappe.get_list("Billing Database Detail", 
                    fields=['*'],
                    filters = required_filter
                )
                if len(list_of_billing_database_data) > 0:
                    return {'status':True,'value':list_of_alt_billing_database_data[0]}
                else:
                    return {'status':False}
            else:
                return {'status':False}
        except:
            return {'status':False}
