import frappe

#application imports
from ..custom_methods.reusable_methods import get_location_lat_long

@frappe.whitelist(allow_guest = True)
def open_meter_readings(meter_reader = None,billing_period = None,billing_area = None):
    '''
    Function that gets all open meter readings
    for a given meter reader,billing area,billing 
    period
    '''
    frappe.set_user("Administrator")
    #intialize filters as empty dictionary
    custom_filters = {'status':'Open'}
    #create filters based on given parameters
    if meter_reader:
        custom_filters['meter_reader'] = meter_reader
    if billing_period:
        custom_filters['billing_period'] = billing_period
    if billing_area:
        custom_filters['billing_area'] = billing_area
    #get meter reading sheets for meter_reader
    open_sheets = frappe.get_list("Meter Reading Sheet",
        filters = custom_filters,
        fields = ['name']
    )

    #initialize return as empty dict
    return_dict = {}
    #loop through the list
    for sheet in open_sheets:
        #get the all meter reading
        sheet_doc = frappe.get_doc("Meter Reading Sheet",sheet["name"])
        #check if meter reading has been added
        if not sheet_doc.name in return_dict.keys():
            return_dict[sheet_doc.name] = {}
        #check if billing area has been added
        if not 'billing_area' in return_dict[sheet_doc.name].keys():
            return_dict[sheet_doc.name]['billing_area'] = sheet_doc.billing_area
        #check if billing period has been added
        if not "billing_period" in return_dict[sheet_doc.name].keys():
            return_dict[sheet_doc.name]["billing_period"] = sheet_doc.billing_period
        
        #initialize sheet details as empty dictionary
        sheet_detail_list = []
        #loop through meter reading details
        for reading_details in sheet_doc.meter_reading_sheet_detail:
            #initialize sheet details as empty dictionary
            sheet_detail = {}
            sheet_detail['name'] = reading_details.meter_reading
            sheet_detail['meter_serial'] = reading_details.meter_serial
            sheet_detail['customer_name'] = reading_details.customer_name
            sheet_detail['last_meter_reading'] = reading_details.last_meter_reading
            sheet_detail['current_meter_reading'] = reading_details.current_meter_reading
            sheet_detail['consumption'] = reading_details.consumption
            sheet_detail['status'] = reading_details.status

            #comment out the latitude and longitude for now
            #now get latitude and longitude from meter details
            cus_details_doc_list = frappe.get_list("Customer Details",
                filters = {
                    'meter':reading_details.meter_serial
                },
                fields = ['name','map_location']
            )
            if len(cus_details_doc_list) > 0:
                # lat_long_values = get_location_lat_long(cus_details_doc_list[0].map_location)
                # sheet_detail['latitude'] = lat_long_values['latitude']
                # sheet_detail['longitude'] = lat_long_values['longitude']
                #append the details to the list
                sheet_detail_list.append(sheet_detail)
                
        #update return dict
        return_dict[sheet_doc.name]['meter_readings'] = sheet_detail_list
    #now return the list
    return return_dict

@frappe.whitelist(allow_guest = True)
def test_api():
	return {'status':True}

       

        

