// Copyright (c) 2021, Upande LTD. and contributors
// For license information, please see license.txt

//list of billing fields
var billing_area_fields = [
	"billing_area_1","billing_area_2","billing_area_3","billing_area_4",
	"billing_area_5","billing_area_6","billing_area_7","billing_area_8",
	"billing_area_9","billing_area_10"
]

//filter fields
function filter_fields(billing_area_field,level_1 = null,billing_area_name = null){
	var filters = {}
	//check level
	if(level_1){
		filters['root_area'] = 1
		//get the root billing area
		frappe.call({
			method: "frappe.client.get_list",
			args:{
					doctype: "Billing Area",
					filters: {
						root_area:1
				},
			fields:["name"]
			},
			callback: function(response) {
				if(response.message.length > 0){
					//level one
					cur_frm.set_query(billing_area_field, function() {
						return {
							"filters": {
								"parent_billing_area": response.message[0]['name']
							}
						}
					})
				}
			}
		})
	}else{
		//level one
		cur_frm.set_query(billing_area_field, function() {
			return {
				"filters": {
					"parent_billing_area": billing_area_name
				}
			}
		})
	}
}

//clear list of fields
function clear_fields(list_of_fields){
	list_of_fields.forEach(field => {
		cur_frm.set_value(field,"")
	});
}

// function that sets custom buttons
function add_custom_buttons(button_name,action){
	cur_frm.add_custom_button(__(button_name), function(){
		//check cur_doc is new
		if(cur_frm.doc.__islocal){
			//throw an error to the customer
			frappe.throw("You need to save the document before running any action")
		}else{
			if(action=="close_reading_sheet"){
				//check if user has privillages
				if(frappe.user.has_role("Administrator") || frappe.user.has_role("Meter Reading Admin")){
					//set status as closed
					cur_frm.set_value("status","Closed")
					cur_frm.save()
				}else{
					frappe.throw("You do not have enough privillages to run this action")
				}
			}else if(action=="open_reading_sheet"){
				//check if user has privillages
				if(frappe.user.has_role("Administrator") || frappe.user.has_role("Meter Reading Admin")){
					//set status as closed
					cur_frm.set_value("status","Open")
					cur_frm.save()
				}else{
					frappe.throw("You do not have enough privillages to run this action")
				}
			}
		}
	},__("Actions"));
}

frappe.ui.form.on('Meter Reading Sheet',{
	refresh: function(frm) {
		//add custom buttons
		add_custom_buttons("Close Reading Sheet","close_reading_sheet")
		add_custom_buttons("Open Reading Sheet","open_reading_sheet")
		//filter billing area fields
		filter_fields("billing_area_1",true)
	}
});

//function that runs when the fetch_meter_reading is clicked
frappe.ui.form.on("Meter Reading Sheet", "fetch_meter_reading", function(frm){
	//set fetching_meter_readings as true
	cur_frm.set_value("fetching_meter_readings",1)
	//now save the document
	cur_frm.save()
});

//billing area 1
frappe.ui.form.on("Meter Reading Sheet", "billing_area_1", function(frm){
	//clear value of the next billing areas
	clear_fields(billing_area_fields.slice(1))
	//set as current billing area
	if(cur_frm.doc.billing_area_1){
		cur_frm.set_value("billing_area",cur_frm.doc.billing_area_1)
		filter_fields("billing_area_2",false,cur_frm.doc.billing_area_1)
	}else{

	}
});

//billing area 2
frappe.ui.form.on("Meter Reading Sheet", "billing_area_2", function(frm){
	//clear value of the next billing areas
	clear_fields(billing_area_fields.slice(2))
	//set as current billing area
	if(cur_frm.doc.billing_area_2){
		cur_frm.set_value("billing_area",cur_frm.doc.billing_area_2)
		filter_fields("billing_area_3",false,cur_frm.doc.billing_area_2)
	}else{
		cur_frm.set_value("billing_area",cur_frm.doc.billing_area_1)
	}
});

//billing area 3
frappe.ui.form.on("Meter Reading Sheet", "billing_area_3", function(frm){
	//clear value of the next billing areas
	clear_fields(billing_area_fields.slice(3))
	//set as current billing area
	if(cur_frm.doc.billing_area_3){
		cur_frm.set_value("billing_area",cur_frm.doc.billing_area_3)
		filter_fields("billing_area_4",false,cur_frm.doc.billing_area_3)
	}else{
		cur_frm.set_value("billing_area",cur_frm.doc.billing_area_2)
	}
});

//billing area 4
frappe.ui.form.on("Meter Reading Sheet", "billing_area_4", function(frm){
	//clear value of the next billing areas
	clear_fields(billing_area_fields.slice(4))
	//set as current billing area
	if(cur_frm.doc.billing_area_4){
		cur_frm.set_value("billing_area",cur_frm.doc.billing_area_4)
		filter_fields("billing_area_5",false,cur_frm.doc.billing_area_4)
	}else{
		cur_frm.set_value("billing_area",cur_frm.doc.billing_area_3)
	}
});

//billing area 5
frappe.ui.form.on("Meter Reading Sheet", "billing_area_5", function(frm){
	//clear value of the next billing areas
	clear_fields(billing_area_fields.slice(5))
	//set as current billing area
	if(cur_frm.doc.billing_area_5){
		cur_frm.set_value("billing_area",cur_frm.doc.billing_area_5)
		filter_fields("billing_area_6",false,cur_frm.doc.billing_area_5)
	}else{
		cur_frm.set_value("billing_area",cur_frm.doc.billing_area_4)
	}
});

//billing area 6
frappe.ui.form.on("Meter Reading Sheet", "billing_area_6", function(frm){
	//clear value of the next billing areas
	clear_fields(billing_area_fields.slice(6))
	//set as current billing area
	if(cur_frm.doc.billing_area_6){
		cur_frm.set_value("billing_area",cur_frm.doc.billing_area_6)
		filter_fields("billing_area_7",false,cur_frm.doc.billing_area_6)
	}else{
		cur_frm.set_value("billing_area",cur_frm.doc.billing_area_5)
	}
});

//billing area 7
frappe.ui.form.on("Meter Reading Sheet", "billing_area_7", function(frm){
	//clear value of the next billing areas
	clear_fields(billing_area_fields.slice(7))
	//set as current billing area
	if(cur_frm.doc.billing_area_7){
		cur_frm.set_value("billing_area",cur_frm.doc.billing_area_7)
		filter_fields("billing_area_8",false,cur_frm.doc.billing_area_7)
	}else{
		cur_frm.set_value("billing_area",cur_frm.doc.billing_area_6)
	}
});

//billing area 8
frappe.ui.form.on("Meter Reading Sheet", "billing_area_8", function(frm){
	//clear value of the next billing areas
	clear_fields(billing_area_fields.slice(8))
	//set as current billing area
	if(cur_frm.doc.billing_area_8){
		cur_frm.set_value("billing_area",cur_frm.doc.billing_area_8)
		filter_fields("billing_area_7",false,cur_frm.doc.billing_area_8)
	}else{
		cur_frm.set_value("billing_area",cur_frm.doc.billing_area_7)
	}
});

//billing area 9
frappe.ui.form.on("Meter Reading Sheet", "billing_area_9", function(frm){
	//clear value of the next billing areas
	clear_fields(billing_area_fields.slice(9))
	//set as current billing area
	if(cur_frm.doc.billing_area_9){
		cur_frm.set_value("billing_area",cur_frm.doc.billing_area_9)
		filter_fields("billing_area_10",false,cur_frm.doc.billing_area_9)
	}else{
		cur_frm.set_value("billing_area",cur_frm.doc.billing_area_8)
	}
});

//billing area 10
frappe.ui.form.on("Meter Reading Sheet", "billing_area_10", function(frm){
	//set as current billing area
	if(cur_frm.doc.billing_area_10){
		cur_frm.set_value("billing_area",cur_frm.doc.billing_area_10)
	}else{
		cur_frm.set_value("billing_area",cur_frm.doc.billing_area_9)
	}
});

