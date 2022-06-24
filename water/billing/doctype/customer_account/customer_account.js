// Copyright (c) 2021, Upande LTD. and contributors
// For license information, please see license.txt

// function that sets custom buttons
function add_custom_buttons(button_name,action){
	cur_frm.add_custom_button(__(button_name), function(){
		//check cur_doc is new
		if(cur_frm.doc.__islocal){
			//throw an error to the customer
			frappe.throw("You need to save the account before running any action")
		}else{
			if(action=="initiate_connection"){
				if(cur_frm.doc.status == "Draft" || cur_frm.doc.status == "Disconnected"
				|| cur_frm.doc.status == "Dormant"){
					//set some values for state transition
					cur_frm.set_value("status_transitioning",1)
					cur_frm.set_value("previous_status",cur_frm.doc.status)
					cur_frm.set_value("status","Pending Connection")
					//save to apply the action
					cur_frm.save()
				}else{
					frappe.throw("This action is only meant for new connection\
					new,disconnected or dormant accounts")
				}
			}else if(action=="connect"){
				if(cur_frm.doc.status == "Pending Connection"){
					//set some values for state transition
					cur_frm.set_value("status_transitioning",1)
					cur_frm.set_value("previous_status",cur_frm.doc.status)
					cur_frm.set_value("status","Connected")
					//save to apply the action
					cur_frm.save()
				}else{
					frappe.throw("This action is only meant for accounts Pending Connection")
				}
			}else if(action=="initiate_activation"){
				if(cur_frm.doc.status == "Connected"){
					//set some values for state transition
					cur_frm.set_value("status_transitioning",1)
					cur_frm.set_value("previous_status",cur_frm.doc.status)
					cur_frm.set_value("status","Pending Activation")
					//save to apply the action
					cur_frm.save()
				}else{
					frappe.throw("This action is only meant for accounts whose status is connected")
				}
			}
			else if (action == "activate"){
				if(cur_frm.doc.status == "Pending Activation" ){
					//set some values for state transition
					cur_frm.set_value("status_transitioning",1)
					cur_frm.set_value("previous_status",cur_frm.doc.status)
					cur_frm.set_value("status","Active")
					//save to apply the action
					cur_frm.save()
				}else{
					frappe.throw("This action is only meant for currently Inactive accounts")
				}
			}else if(action=="deactivate"){
				if(cur_frm.doc.status == "Active"){
					//set some values for state transition
					cur_frm.set_value("status_transitioning",1)
					cur_frm.set_value("previous_status",cur_frm.doc.status)
					cur_frm.set_value("status","Pending Activation")
					//save to apply the action
					cur_frm.save()
				}else{
					frappe.throw("This action is only meant currently Active accounts")
				}
			} else if(action=="initiate_disconnection"){
				if(cur_frm.doc.status == "Active"){
					//set some values for state transition
					cur_frm.set_value("status_transitioning",1)
					cur_frm.set_value("previous_status",cur_frm.doc.status)
					cur_frm.set_value("status","Pending Disconnection")
					//save to apply the action
					cur_frm.save()
				}else{
					frappe.throw("This action is only meant currently Active accounts")
				}
			}else if(action=="disconnect"){
				if(cur_frm.doc.status == "Pending Disconnection"){
					//set some values for state transition
					cur_frm.set_value("status_transitioning",1)
					cur_frm.set_value("previous_status",cur_frm.doc.status)
					cur_frm.set_value("status","Disconnected")
					//save to apply the action
					cur_frm.save()
				}else{
					frappe.throw("This action is only meant for acounts Pending Disconnection")
				}
			}else if(action == "initiate_permnanent_disconnection"){
				//initiate disconnection from main
				if(cur_frm.doc.status == "Disconnected"){
					//set some values for state transition
					cur_frm.set_value("status_transitioning",1)
					cur_frm.set_value("previous_status",cur_frm.doc.status)
					cur_frm.set_value("status","Pending Permanent Disconnection")
					//save to apply the action
					cur_frm.save()
				}else{
					frappe.throw("This action is only meant for Disconnected acounts")
				}
			}else if(action == "disconnect_permanently"){
				//mark as dormant
				if(cur_frm.doc.status == "Pending Permanent Disconnection"){
					//set some values for state transition
					cur_frm.set_value("status_transitioning",1)
					cur_frm.set_value("previous_status",cur_frm.doc.status)
					cur_frm.set_value("status","Dormant")
					//save to apply the action
					cur_frm.save()
				}else{
					frappe.throw("This action is only meant for acounts Pending Permanent Disconnection")
				}
			}
		}
	},__("Actions"));
}


frappe.ui.form.on('Customer Account', {
	refresh: function(frm) {
		cur_frm.add_custom_button(__("View Customer Details"), viewCustomerDetails);

		add_custom_buttons("Initiate Connection","initiate_connection");
		add_custom_buttons("Connect","connect");
		add_custom_buttons("Initiate Activation","initiate_activation");
		add_custom_buttons("Activate","activate");
		add_custom_buttons("Deactivate","deactivate");
		add_custom_buttons("Initiate Disconnection","initiate_disconnection");
		add_custom_buttons("Disconnect","disconnect");
		add_custom_buttons("Initiate Permanent Disconnection","initiate_permnanent_disconnection");
		add_custom_buttons("Mark as Dormant","disconnect_permanently");
	}
});


const viewCustomerDetails = () => {
	//get customer details
	frappe.call({
		method: "frappe.client.get_list",
		args:{
			doctype: "Customer Details",
			filters: {
				"details_status":"Current",
				"linked_customer_account":cur_frm.doc.name
		},
		fields:["name"]
		},
		callback: function(response) {
			if(response.message.length > 0){
				let detailsDocName = response.message[0].name
				//redirect to customer details document
				frappe.set_route('Form', 'Customer Details',detailsDocName)
			}else{
				frappe.throw("A customer details document for this account has not be generated")
			}
		}
	});
}