// Copyright (c) 2021, Upande LTD. and contributors
// For license information, please see license.txt

// function that sets custom buttons
function add_custom_buttons(button_name,action){
	cur_frm.add_custom_button(__(button_name), function(){
		//check cur_doc is new
		if(cur_frm.doc.__islocal){
			//throw an error to the customer
			frappe.throw("You need to save the task before running any action")
		}else{
			if(action=="close"){
				//set the document status as closed
				cur_frm.set_value("status","Closed");
				cur_frm.save()
			}else if(action=="open"){
				//set the document status as closed
				cur_frm.set_value("status","Open");
				cur_frm.save()
			}else if (action=="cancel"){
				//set the document status as closed
				cur_frm.set_value("status","Cancelled");
				cur_frm.save()
			}
		}
	},__("Actions"));
};

frappe.ui.form.on('Company Task', {
	refresh: function(frm) {
		//add action buttons
		add_custom_buttons("Close Task","close")
		add_custom_buttons("Open Task","open")
		add_custom_buttons("Cancel Task","cancel")
	}
});
