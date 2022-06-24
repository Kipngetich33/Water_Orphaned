import frappe
from washmis_erp.washmis_erp_license import Licensing

@frappe.whitelist(allow_guest=True)
def check_licensing_status():
    '''
    Function that checks the licensing status of 
    Washmis ERP 
    input:
        None
    output:
        dict - {'status':True/False,details:{}}
    '''
    status = True #initialize license status to True
    details = {'status':status,'updates':0,'message':''}

    # create a Licensing instance
    washmis_erp_setting_obj = Licensing()
    # check if a license is required
    if not washmis_erp_setting_obj.check_if_license_is_required():
        details['status'] = True
        details['message'] = 'No license required'
        return details
    else:
        # check if license is a valid
        if washmis_erp_setting_obj.check_license_status():
            details['status'] = True
            details['message'] = 'License is valid'
            return details
        else:
            details['status'] = False
            details['message'] = 'License is invalid'
            return details


@frappe.whitelist(allow_guest=True)
def check_for_updates():
    '''
    Function that checks if updates from Washmis ERP exist
    input:
        None
    output:
        boolean - True/False
    '''
    # create a Licensing instance
    washmis_erp_setting_obj = Licensing()
    # check if updates exist
    if washmis_erp_setting_obj.check_for_updates():
        return True
    else:
        return False

@frappe.whitelist(allow_guest=True)
def check_license_key_is_valid(license_key):
    '''
    Function that checks that a given license 
    key is valid then updates the license 
    input:
        varchar - license_key
    output:
        bolean - True/False
    '''
    return_status = False
    # create a Licensing instance
    washmis_erp_setting_obj = Licensing()
    # check if key is valid
    license_validity = washmis_erp_setting_obj.check_license_key_is_valid(license_key)
    if license_validity['status']:
        # update license time
        return_status = True
        # add license time to global 
        washmis_erp_setting_obj.add_license_time(license_validity['license_time'])
    else:
        return_status = False
    
    # return the status
    return return_status
