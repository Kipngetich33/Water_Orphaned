import frappe

#app import
from .reusable_methods import create_bill,create_company_task_from_common_task

def initiate_new_connection(customer_account_doc):
    '''
    Function that initiates the process of a new customer 
    connection 
    input:
        cls object - customer_account_doc
    output:
        None of now
    ''' 
    #create connection bill if required
    if customer_account_doc.billing_settings.initial_connection_fees_required:
        #prepare parameters for the  create_bill function
        customer_account_name = customer_account_doc.name
        bill_type = "New Connection Fee"
        bill_item = customer_account_doc.billing_settings.connection_amount
        bill_items_list = [{'bill_item':bill_item,'quantity':1}]
	    #create a new connection bill
        create_bill(customer_account_name,bill_type,bill_items_list)

    #create various todos for customer conenction
    if customer_account_doc.billing_settings.connection_task:
        #create a new connection task
        connection_task = customer_account_doc.billing_settings.connection_task
        task_name = "New Connection - {}".format(customer_account_doc.full_name)
        create_company_task_from_common_task(task_name,connection_task,customer_account_doc.name,"New Connection")

def initiate_account_reconnection(customer_account_doc):
    '''
    Function that initiates the process of account 
    reconnection 
    input:
        cls object - customer_account_doc
    output:
        None of now
    '''
    #create reconnection bill if required
    if customer_account_doc.billing_settings.fees_required_after_temporary_disconnection\
    or customer_account_doc.billing_settings.fee_required_after_permanent_disconnection:
        #prepare parameters for the  create_bill function
        customer_account_name = customer_account_doc.name
        bill_type = "Reconnection Fee"
        if customer_account_doc.previous_status == "Disconnected":
            bill_item = customer_account_doc.billing_settings.reconnection_amount_after_temporary_disconnection
        elif customer_account_doc.previous_status == "Dormant":
            bill_item = customer_account_doc.billing_settings.reconnection_amount_after_permanent_disconnection

        bill_items_list = [{'bill_item':bill_item,'quantity':1}]
	    #create a new connection bill
        create_bill(customer_account_name,bill_type,bill_items_list)
        
    #create various todos for customer conenction
    if customer_account_doc.billing_settings.reconnection_task_after_temporary_disconnection\
    or customer_account_doc.billing_settings.reconnection_amount_after_permanent_disconnection:
        #create a reconnection task
        if customer_account_doc.previous_status == "Disconnected":
            reconnection_task = customer_account_doc.billing_settings.reconnection_task_after_temporary_disconnection
        elif customer_account_doc.previous_status == "Dormant":
            reconnection_task = customer_account_doc.billing_settings.reconnection_task_after_permanent_disconnection

        task_name = "Reconnection - {}".format(customer_account_doc.full_name)
        create_company_task_from_common_task(task_name,reconnection_task,customer_account_doc.name,"Reconnection")

def initiate_acc_activation(customer_account_doc):
    '''
    Function that initiates the process of a customer 
    account activation 
    input:
        cls object - customer_account_doc
    output:
        None of now
    '''
    #create activation bill if required
    if customer_account_doc.billing_settings.activation_fees_required:
        #prepare parameters for the  create_bill function
        customer_account_name = customer_account_doc.name
        bill_type = "Activation Fee"
        bill_item = customer_account_doc.billing_settings.activation_amount
        bill_items_list = [{'bill_item':bill_item,'quantity':1}]
	    #create a new activation bill
        create_bill(customer_account_name,bill_type,bill_items_list)

    #create various todos for customer conenction
    if customer_account_doc.billing_settings.activation_task:
        #create a new connection task
        activation_task = customer_account_doc.billing_settings.activation_task
        task_name = "Activation - {}".format(customer_account_doc.full_name)
        create_company_task_from_common_task(task_name,activation_task,customer_account_doc.name,"Activation")

def initiate_acc_disconnection(customer_account_doc):
    '''
    Function that initiates the process of a customer 
    account disconnection 
    input:
        cls object - customer_account_doc
    output:
        None of now
    '''
    #create various todos for customer disconenction
    if customer_account_doc.billing_settings.disconnection_task:
        #create a new connection task
        disconnection_task = customer_account_doc.billing_settings.disconnection_task
        task_name = "Disconnection - {}".format(customer_account_doc.full_name)
        create_company_task_from_common_task(task_name,disconnection_task,customer_account_doc.name,"Disconnection")

def initiate_permanent_acc_disconnection(customer_account_doc):
    '''
    Function that initiates the process of permanent customer 
    account disconnection i.e making an account dormant 
    input:
        cls object - customer_account_doc
    output:
        None of now
    '''
    #create various todos for customer disconenction
    if customer_account_doc.billing_settings.permanent_disconnection_task:
        #create a new permnanent disconnection task
        permanent_disconnection_task = customer_account_doc.billing_settings.permanent_disconnection_task
        task_name = "Permanent Disconnection - {}".format(customer_account_doc.full_name)
        create_company_task_from_common_task(task_name,permanent_disconnection_task,customer_account_doc.name,"Permanent Disconnection")

def validate_account_connection(customer_acc_doc):
    '''
    Function that checks to ensure all the connection requirements
    are met before the account status is changed to connected
    '''
    #check that all the connection todos have been completed
    if customer_acc_doc.billing_settings.connection_task:
        #check that connection todos have been completed
        connection_task_list = frappe.get_list('Company Task',
                                    filters = [['customer_account','=',customer_acc_doc.name],
                                        ['task_type','=','New Connection'],
                                        ['status','!=','Closed'],
                                        ['status','!=','Cancelled']
                                    ],
							fields = ['name']
						)

        #check if any connection todo is not complete
        if len(connection_task_list) > 0:
            #get the doc n url
            task_doc = frappe.get_doc("Company Task",connection_task_list[0].name)
            task_url = task_doc.get_url().replace(" ","%20")
            frappe.throw("New Connection Task <a style='color:blue;' href={}>{}</a> has not be closed"\
                .format(task_url,task_doc.name))

    #check that connection fee has been paid
    if customer_acc_doc.billing_settings.initial_connection_fees_required:
        #then check if the bill has been paid
        connection_bill_list = frappe.get_list('Bill', filters = {
							'bill_type': "New Connection Fee",
                            'customer_account':customer_acc_doc.name,
                            'status':'Unpaid'
							},fields = ['name']
						)
        if len(connection_bill_list) > 0:
            #get the doc n url
            bill_doc = frappe.get_doc("Bill",connection_bill_list[0].name)
            frappe.throw("New Connection Fee Bill <a style='color:blue;' href={}>{}</a>  has not been paid"\
                .format(bill_doc.get_url(),bill_doc.name))

    #check that customer details document has been created for customer
    if customer_acc_doc.customer_details:
        #get the link customer details document
        cus_details_doc = frappe.get_doc("Customer Details",customer_acc_doc.customer_details)
        cus_details_url = cus_details_doc.get_url().replace(" ","%20")
        #check if meter is connected and working properly
        if cus_details_doc.meter_status == "Connected":
            pass
        else:
            frappe.throw('A meter has not be connected for the customer account {}\
                .Please check the customer details document <a href="{}">{}</a>\
                '.format(customer_acc_doc.name,cus_details_url,cus_details_doc.name))
    else:
        frappe.throw("A customer details document does not exist for Customer Account {}\
            ".format(customer_acc_doc.name))

def validate_account_reconnection(customer_acc_doc):
    '''
    Function that checks to ensure all the reconnection requirements
    are met before the account status is changed to connected
    '''
    #check that all the connection todos have been completed
    if customer_acc_doc.billing_settings.reconnection_task:
        #check that reconnection todos have been completed
        task_list = frappe.get_list('Company Task',
                                    filters = [['customer_account','=',customer_acc_doc.name],
                                        ['task_type','=','Reconnection'],
                                        ['status','!=','Closed'],
                                        ['status','!=','Cancelled']
                                    ],
							fields = ['name']
						)

        #check if any reconnection todo is not complete
        if len(task_list) > 0:
            #get the doc n url
            task_doc = frappe.get_doc("Company Task",task_list[0].name)
            task_url = task_doc.get_url().replace(" ","%20")
            frappe.throw("Reconnection Task <a style='color:blue;' href={}>{}</a> has not be closed"\
                .format(task_url,task_doc.name))

    #check that reconnection fee has been paid
    if customer_acc_doc.billing_settings.initial_connection_fees_required:
        #then check if the bill has been paid
        bill_list = frappe.get_list('Bill', filters = {
							'bill_type': "Reconnection Fee",
                            'customer_account':customer_acc_doc.name,
                            'status':'Unpaid'
							},fields = ['name']
						)
        if len(bill_list) > 0:
            #get the doc n url
            bill_doc = frappe.get_doc("Bill",bill_list[0].name)
            frappe.throw("The Ronnection Fee Bill <a style='color:blue;' href={}>{}</a>  has not been paid"\
                .format(bill_doc.get_url(),bill_doc.name))

    #check that customer details document has been created for customer
    if customer_acc_doc.customer_details:
        #get the link customer details document
        cus_details_doc = frappe.get_doc("Customer Details",customer_acc_doc.customer_details)
        cus_details_url = cus_details_doc.get_url().replace(" ","%20")

        #check if meter is connected and working properly
        if cus_details_doc.meter_status == "Connected":
            pass
        else:
            frappe.throw('A meter has not be connected for the customer account {}\
                .Please check the customer details document <a href="{}">{}</a>\
                '.format(customer_acc_doc.name,cus_details_url,cus_details_doc.name))
    else:
        frappe.throw("A customer details document does not exist for Customer Account {}\
            ".format(customer_acc_doc.name))

def validate_account_activation(customer_acc_doc):
    '''
    Function that checks to ensure all the activation requirements
    are met before the account is activated
    '''
    #check that all the todos have been completed
    if customer_acc_doc.billing_settings.activation_task:
        #check that Activation tasks have been completed
        task_list = frappe.get_list('Company Task',
                                    filters = [['customer_account','=',customer_acc_doc.name],
                                        ['task_type','=','Activation'],
                                        ['status','!=','Closed'],
                                        ['status','!=','Cancelled']
                                    ],
							fields = ['name']
						)

        #check if any Activation tasks is not complete
        if len(task_list) > 0:
            #get the doc n url
            task_doc = frappe.get_doc("Company Task",task_list[0].name)
            task_url = task_doc.get_url().replace(" ","%20")
            frappe.throw("The activation Task <a style='color:blue;' href={}>{}</a> has not be closed"\
                .format(task_url,task_doc.name))

    #check that activation fee has been paid
    if customer_acc_doc.billing_settings.activation_fees_required:
        #then check if the bill has been paid
        connection_bill_list = frappe.get_list('Bill', filters = {
							'bill_type': "Activation Fee",
                            'customer_account':customer_acc_doc.name,
                            'status':'Unpaid'
							},fields = ['name']
						)
        if len(connection_bill_list) > 0:
            #get the doc n url
            bill_doc = frappe.get_doc("Bill",connection_bill_list[0].name)
            frappe.throw("The activation Fee Bill <a style='color:blue;' href={}>{}</a>  has not been paid"\
                .format(bill_doc.get_url(),bill_doc.name))

    #check that customer details document has been created for customer
    if customer_acc_doc.customer_details:
        #get the link customer details document
        cus_details_doc = frappe.get_doc("Customer Details",customer_acc_doc.customer_details)
        #check an ERPNext customer has been created for the customer account
        if cus_details_doc.customer:
            #now check that customer account is enabled
            erp_cus_doc = frappe.get_doc("Customer",cus_details_doc.customer)
            if erp_cus_doc.disabled == 0:
                pass
            else:
                frappe.throw("The customer {} linked to this customer account {} is disabled\
                    .Please check the customer details document".format(erp_cus_doc.name,cus_details_doc.name))
        else:
            frappe.throw('No customer is linked with the Customer Account {}\
                .Please check the customer details document'.format(customer_acc_doc.name))

        #check customer type has been specified
        if not cus_details_doc.customer_type:
            frappe.throw("The Customer Type has not be defined.Please check the Customer Details document")

        #check billing area details are confirmed
        if cus_details_doc.billing_area_confirmation != "Confirmed":
            frappe.throw("Billing Area details have not be confirmed in customer details")
        #check connection details section is confirmed
        if cus_details_doc.meter_status != "Connected":
            frappe.throw("A Meter has not be connected for this customer account under customer details")
        #check sanitation section details are confirmed
        if cus_details_doc.sanitation_details_confirmation != "Confirmed":
            frappe.throw("Sanitation details have not been confirmed, check customer details")
        #check GPS details section details are confirmed
        if cus_details_doc.gps_coordinates_confirmed != "Confirmed":
            frappe.throw("GPS Coordinates have not been confirmed,check customer details")

    else:
        frappe.throw("A customer details document does not exist for Customer Account {}\
            ".format(customer_acc_doc.name))

    

def validate_account_disconnection(customer_acc_doc):
    '''
    Function that checks to ensure all the disconnection requirements
    are met before the account is disconnected
    '''
    #check that all the tasks have been completed
    if customer_acc_doc.billing_settings.disconnection_task:
        #check that Activation tasks have been completed
        pass
        task_list = frappe.get_list('Company Task',
                                    filters = [['customer_account','=',customer_acc_doc.name],
                                        ['task_type','=','Disconnection'],
                                        ['status','!=','Closed'],
                                        ['status','!=','Cancelled']
                                    ],
							fields = ['name']
						)

        #check if any disconnection tasks is not complete
        if len(task_list) > 0:
            #get the doc n url
            task_doc = frappe.get_doc("Company Task",task_list[0].name)
            task_url = task_doc.get_url().replace(" ","%20")
            frappe.throw("The disconnection Task <a style='color:blue;' href={}>{}</a> has not be closed"\
                .format(task_url,task_doc.name))

    #check that meter has been disconnected
    if customer_acc_doc.customer_details:
        #get the link customer details document
        cus_details_doc = frappe.get_doc("Customer Details",customer_acc_doc.customer_details)
        cus_details_url = cus_details_doc.get_url().replace(" ","%20")
        #check if meter is has been disconnected
        if cus_details_doc.meter_status == "Disconnected":
            pass
        else:
            frappe.throw('A meter linked to the customer account {} has not been disconnected\
                .Please check the <a href="{}">Customer Details</a> document\
                '.format(customer_acc_doc.name,cus_details_url))
    else:
        frappe.throw("A customer details document does not exist for Customer Account {}\
            ".format(customer_acc_doc.name))

def validate_permanent_account_disconnection(customer_acc_doc):
    '''
    Function that checks to ensure all the permanent disconnection requirements
    are met before the account is mark as dormant
    '''
    #check that all the tasks have been completed
    if customer_acc_doc.billing_settings.permanent_disconnection_task:
        #check that all permanent disconnection tasks have been completed
        pass
        task_list = frappe.get_list('Company Task',
                                    filters = [['customer_account','=',customer_acc_doc.name],
                                        ['task_type','=','Permanent Disconnection'],
                                        ['status','!=','Closed'],
                                        ['status','!=','Cancelled']
                                    ],
							fields = ['name']
						)

        #check if any permanent disconnection tasks is not complete
        if len(task_list) > 0:
            #get the doc n url
            task_doc = frappe.get_doc("Company Task",task_list[0].name)
            task_url = task_doc.get_url().replace(" ","%20")
            frappe.throw("The permanent disconnection Task <a style='color:blue;' href={}>{}</a> has not be closed"\
                .format(task_url,task_doc.name))

    #check that meter has been completely disconnected
    if customer_acc_doc.customer_details:
        #get the link customer details document
        cus_details_doc = frappe.get_doc("Customer Details",customer_acc_doc.customer_details)
        cus_details_url = cus_details_doc.get_url().replace(" ","%20")
        #check if meter is has been disconnected
        if cus_details_doc.meter_status == "Disconnected" and \
        cus_details_doc.disconnection_level == 3:
            pass
        else:
            frappe.throw('A meter linked to the customer account {} has not been permanently disconnected\
                .Please check the <a href="{}">Customer Details</a> document\
                '.format(customer_acc_doc.name,cus_details_url))
    else:
        frappe.throw("A customer details document does not exist for Customer Account {}\
            ".format(customer_acc_doc.name))







    