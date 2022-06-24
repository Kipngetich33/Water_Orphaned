import frappe

#application level imports
from notification.sms.custom_methods.send_sms import SMSClass
from erpnext.accounts.utils import get_balance_on
from water.custom_methods.reusable_methods import get_settings

def update_bill(doc,method):
    '''
    Function that updates the values of the 
    bill once the bill is payed
    '''
    #get related bill item
    related_bill_list = frappe.get_list("Bill",filters = {
        'linked_sales_invoice':doc.name
    })
    #check if there is related bill list
    if not related_bill_list:
        return 
    #get the name of the bill
    bill_doc = frappe.get_doc("Bill",related_bill_list[0]['name'])
    #check if both statuses are the same
    if doc.status == bill_doc.status:
        pass
    else:
        #check if status is paid
        if doc.status == "Paid":
            bill_doc = doc.status
            #saved changes
            bill_doc.save(ignore_permissions = True)
            frappe.db.commit()

def test(doc,method):
    return 

def payment_submission(doc,method):
    #loop through linked invoices
    for invoice in doc.references:
        #resolve status of related bills
        reconcile_bill_status(invoice)
    #send customer notifications of 
    #their remainig balance
    notify_customer_of_their_balance(doc)

def payment_reconcilliation(doc,method):
    #loop through linked invoices
    for invoice in doc.references:
        #resolve status of related bills
        if doc.status == "Submitted":
            reconcile_bill_status(invoice)
        elif doc.status == "Cancelled":
            # payment_reconcilliation_on_cancel(invoice)
            pass

def reconcile_bill_status(sales_invoice):
    '''
    Function that gets bill linked to a given 
    sales invoice and reconcile their statuses
    '''
    #get sales invoices doc
    try:
        sales_invoice_doc = frappe.get_doc("Sales Invoice",sales_invoice.reference_name)
        #get related bill
        related_bills = frappe.get_list("Bill",filters = {
            'linked_sales_invoice':sales_invoice_doc.name,
        })
        #check if any invoices were attached
        if len(related_bills) == 0:
            return #return if no invoices are attached

        #get bill document
        bill_doc = frappe.get_doc("Bill",related_bills[0].get('name'))
        #check invoice status
        if sales_invoice_doc.status == "Paid":
            if bill_doc.status == "Paid":
                pass
            else:
                #change status to paid
                bill_doc.status = "Paid"
                bill_doc.save(ignore_permissions = True)
                frappe.db.commit()
        else:
            #check that bill status is not paid
            if bill_doc.status == "Paid":
                #change status to unpaid
                bill_doc.status = "Unpaid"
                bill_doc.save(ignore_permissions = True)
                frappe.db.commit()
    except:
        pass

def payment_reconcilliation_on_cancel(doc,method):
    '''
    Function that gets bill linked to a given 
    sales invoice and reconcile their statuses
    '''
    #get sales invoices doc
    try:
        sales_invoice_doc = frappe.get_doc("Sales Invoice",sales_invoice.reference_name)
        #get related bill
        related_bills = frappe.get_list("Bill",filters = {
            'linked_sales_invoice':sales_invoice_doc.name,
        })
        #check if any invoices were attached
        if len(related_bills) == 0:
            return #return if no invoices are attached

        #get bill document
        bill_doc = frappe.get_doc("Bill",related_bills[0].get('name'))
        #check invoice status
        if sales_invoice_doc.status == "Paid":
            if bill_doc.status == "Paid":
                pass
            else:
                #change status to paid
                bill_doc.status = "Paid"
                bill_doc.save(ignore_permissions = True)
                frappe.db.commit()
        else:
            #check that bill status is not paid
            if bill_doc.status == "Paid":
                #change status to unpaid
                bill_doc.status = "Unpaid"
                bill_doc.save(ignore_permissions = True)
                frappe.db.commit()
    except:
        pass
        
def check_invoice_cancellation(doc,method):
    '''
    Function that checks if a sales invoice is linked
    to a sales invoice and prevents its cancellation
    '''
    #check if user is cancelling sales invoice
    if doc.status != "Cancelled":
        return # status is not cancellation hence 
    related_bills = frappe.get_list("Bill",filters = {
            'linked_sales_invoice':doc.name,
        })
    if len(related_bills) > 0:
        frappe.throw("You cannot cancel a Sales Invoice linked to a Bill.\
            <hr>This Sales Invoice is linked to the bill {}\
            ".format(related_bills[0].get('name')))


def notify_customer_of_their_balance(payment_entry):
    '''
    Function that sends a balance notification to the
    customer
    '''
    #check the linked customer is the uncategorized customer
    if payment_entry.party_name == "Uncategorized Customer":
        #if customer is uncategirized do not send notifications
        return 

    #get mobile money settings
    mobile_money_settings = get_settings("Mobile Payment Settings")
    #get customer details
    customer_details_doc = frappe.get_list("Customer Details",filters ={
                'customer':payment_entry.party,
                'details_status':'Current'
            },
            fields = ['name','customer_phone_number','customer_email']
        )
    #get customer phone number
    customer_phone_number = customer_details_doc[0]['customer_phone_number']
    formated_number = "+254"+customer_phone_number[1:]

    #get account details
    outstading_balance = 0
    account_balance = 0
    party_balance = get_balance_on(None,None,'Customer',payment_entry.party,None)
    if party_balance > 0:
        outstading_balance = party_balance
    elif party_balance < 0:
        account_balance = abs(party_balance)

    #generate message
    message = "Dear Customer your payment of {} has been recived.\
        Your outstading balance is {} and your account balance is {}.\
        ".format(payment_entry.paid_amount,outstading_balance,account_balance)
    #call to action message added only where applicable
    call_to_action_message =  "Please clear your oustanding balance of {}\
        through {}:{} thanks.".format(outstading_balance,\
        mobile_money_settings.transaction_type,mobile_money_settings.mpesa_shortcode)
    #check condition
    if outstading_balance > 0:
       message += call_to_action_message
    else:
        message += "Your current bill has therefore been cleared.Thanks for\
				being a valued customer."
    # message from 
    message += "Regards {}".format(mobile_money_settings.company)

    #send notitification as a background job
    sms_instance = SMSClass()
    sms_instance.message_sending_handler(message,[formated_number])
    







