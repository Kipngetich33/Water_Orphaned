from re import S
import frappe,json

def validate_fields(list_of_required_fields):
    '''
    Function that uses a given lists of fields 
    to determine field values are valid
    input:
        list - with format [
            {'field_name','xxx',value: ....}
        ]
    output:
        dict - with format 
            {'status':True/False,message:str}
    '''
    return_value = {'status':True,'message':''}
    for single_field in list_of_required_fields:
        #check if required
        if single_field['saving_required']:
            #check if value available
            if single_field['value']:
                pass
            else:
                return_value['status'] = False
                return_value['message'] ="The field {} is required"\
                    .format(single_field['field_name'])
                #now return the value
                return return_value
        else:
            pass
    #if no return is executed upto this point
    return return_value

def error_handler(status_dict):
    '''
    Function checks the status based on 
    a dict and throws an error realtime
    input:
        dict - {status:True/False,message:str}
    output:
        frappe error alert is status is false
    '''
    if not status_dict['status']:
        frappe.throw(status_dict['message'])

def get_settings(settings_name):
    '''
    Function that returns the single doctype
    based on the given name
    '''
    return frappe.get_single(settings_name)

def create_bill(customer_acc,bill_type,bill_items_list,extra_fields = None):
    '''
    Function that creates new bill and assigns 
    to a given user
    input:
        customer_acc  -str
        bill_type - str
        bill_items_list -list in format: [
            {'bill_item':'xxxx','quantity':x}
        ]
        extra_fields - list of dictionaries
    '''
    #bill doc
    bill_doc = frappe.new_doc("Bill")
    bill_doc.customer_account = customer_acc
    bill_doc.bill_type = bill_type
    #check if extra fields exists
    if extra_fields:
        #add them
        for extra_field in extra_fields:
            setattr(bill_doc, extra_field['field'], extra_field['value'])
    #loop through all the given bill items
    for bill_item in bill_items_list:
        row = bill_doc.append("bill_item_details", {})
        row.bill_item = bill_item['bill_item']
        row.quantity = bill_item['quantity']
    
    #now save the bill
    bill_doc.save(ignore_permissions = True)
    frappe.db.commit()

def create_single_company_task(task_details):
    '''
    Function that takes in Company Task 
    parameters and uses the to create a
    company task
    input:
        cls obj - Common Task Detail
    output:
        str - Company Task Name
    '''
    #create new Company Task Doc
    task_doc = frappe.new_doc("Company Task")
    #add details to the task
    task_doc.task_name = task_details.task_name
    task_doc.estimate_turnaround_time_in_days = task_details.turnaround_estimate_in_days
    task_doc.description = task_details.description
    #now save the document to database
    task_doc.save(ignore_permissions=True)
    frappe.db.commit()
    #now return the name of the created company task
    return task_doc

def create_child_company_tasks(self,common_task):
    '''
    Function that takes in a common task 
    and uses the child tasks to create 
    child company tasks
    '''
    self.is_group = 1
    if self.tasks_created:
        return

    #loop through all the child tasks 
    for task in common_task.common_task_detail:
        task_doc = create_single_company_task(task)
    	#create a child task for each 
        row = self.append("company_task_detail", {})
        row.task_name = task_doc.name
        row.title = task_doc.task_name
        row.status = task_doc.status
        row.turnaround_estimate_in_days = task_doc.estimate_turnaround_time_in_days
        row.description = task_doc.description
        
    #mark the tasks as created
    self.tasks_created = 1

def create_company_task_from_common_task(task_name,common_task,customer_acc=None,task_type=None):
    '''
    Function that creates a company using a given
    common task
    input:
        common_task - str
    ouput:
        None
    '''
    company_task = frappe.new_doc("Company Task")
    company_task.task_name = task_name
    company_task.created_from_common_tasks = 1
    company_task.common_task = common_task
    company_task.task_type = task_type
    company_task.description = task_name
    #check if customer account is given
    if customer_acc:
        company_task.customer_account = customer_acc
    #now commit to the database
    company_task.save(ignore_permissions=True)
    frappe.db.commit()

def validate_test():
    try:
        doc = frappe.get_doc("Company Task")
        doc.validate()
    except Exception as e:
        print("An error occured {}".format(e))

@frappe.whitelist()
def get_document_url(doc_name,doctype):
    '''
    Function that gets the url of given document and 
    returns it
    input:
        doc_name -str,
        doctype - str
    output:
        'url': xxx - str
    '''
    doc = frappe.get_doc(doctype,doc_name)
    return doc.get_url()

def get_customers_of_billing_area(billing_area_name):
    '''
    Function that fetches all the customers belonging 
    to a non group area 
    input:
        str - billing_area
    output:
    '''
    list_of_customers = frappe.get_list("Customer Details",
            filters = {
                'billing_area':billing_area_name,
                'details_status':'Current'
            },
            fields = ['*']
        )
    #now return the list of customers
    return list_of_customers

def get_non_group_billing_areas(billing_area_name):
    '''
    Function that gets all the none group nodes
    from a given billing area
    input:
        str - billing_area_name
    output:
    '''
    #initiliaze as empty
    none_group_nodes = []
    #get billing_area_name
    billing_area_name_doc = frappe.get_doc("Billing Area",billing_area_name)
    #check if billing area is group
    if billing_area_name_doc.is_group:
        group_nodes = {billing_area_name:billing_area_name_doc.__dict__}
    else:
        group_nodes = {}
        none_group_nodes.append(billing_area_name)

    #now loop through the list of group nodes
    while group_nodes:
        #get the keys
        current_key = list(group_nodes.keys())[0]
        group_nodes.pop(current_key)
        #get all child nodes
        list_of_areas = get_billing_area_children(current_key)
        #now loop through list of areas
        for area in list_of_areas:
            if area['is_group']:
                #append to group nodes
                group_nodes[area['name']] = area
            else:
                none_group_nodes.append(area['name'])

    #now return the billing area child nodes
    return none_group_nodes

def get_billing_area_children(billing_area_name):
    '''
    Function that gets the child nodes of a billing 
    area
    '''
    return frappe.get_list("Billing Area",
            filters = {
                'parent_billing_area':billing_area_name
            },
            fields = ['name','is_group']
        )

def get_erpnext_customer_from_customer_account(cus_acc):
    '''
    Function that gets a erpnext customer account
    linked to a customer account
    input:
        str - cus_acc
    output:
        dict - {'status':boolean, 'customer' : 'xxx'}
    '''
    list_of_customer_accounts = frappe.get_list("Customer Details",
        filters = {
            'details_status':'Current',
            'linked_customer_account':cus_acc
        },
        fields = ['name','customer']
    )
    if list_of_customer_accounts:
        return {'status':True,
            'customer':list_of_customer_accounts[0]['customer']
        }
    else:
        return {'status':False}

def get_location_lat_long(geolocation_field):
    '''
    Function that uses data from the geo location 
    field to get lat,long values
    '''
    try:
    #convert string to dictionary
        location_dict = json.loads(geolocation_field)
        longitude = location_dict['features'][0]['geometry']['coordinates'][0]
        latitude = location_dict['features'][0]['geometry']['coordinates'][1]
        #now return lat,long
        return {'latitude':latitude,'longitude':longitude}
    except:
        return {'latitude':None,'longitude':None}








