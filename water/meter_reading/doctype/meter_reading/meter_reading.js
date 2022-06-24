// Copyright (c) 2021, Upande LTD. and contributors
// For license information, please see license.txt

// function that sets custom buttons
function add_custom_buttons(button_name,action){
	cur_frm.add_custom_button(__(button_name), function(){
		//check cur_doc is new
		if(cur_frm.doc.__islocal){
			//throw an error to the customer
			frappe.throw("You need to save the document before running any action")
		}else{
			if(action=="close_meter_reading"){
				//check if user has privillages
				if(frappe.user.has_role("Administrator") || frappe.user.has_role("Meter Reading Admin")){
					//set status as closed
					cur_frm.set_value("status","Closed")
					cur_frm.save()
				}else{
					frappe.throw("You do not have enough privillages to run this action")
				}
			}
		}
	},__("Actions"));
}


frappe.ui.form.on('Meter Reading', {
	refresh: function(frm) {
		add_custom_buttons("Close Meter Reading","close_meter_reading")
	}
});

//functions that runs when the confirm_readings button is clicked
frappe.ui.form.on("Meter Reading", "confirm_readings", function(frm){
	//check if user has privillages
	if(frappe.user.has_role("Administrator") || frappe.user.has_role("Meter Reading Admin")){
		//check if irregular readings are given
		if(cur_frm.doc.reason_for_irregular_reading){
			cur_frm.set_value("confirm_irregular_reading",1)
			cur_frm.set_value('readings_confirmed_by',frappe.session.user)
			cur_frm.save()
		}else{
			frappe.throw("You need to state the reasons for confirming irregular readings")
		}
	}else{
		frappe.throw("You do not have enough privillages to run this action")
	}
});