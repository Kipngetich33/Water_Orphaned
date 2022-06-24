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


//function that sets the value of field
function clear_field(field_name,value){
	//set it to "" or 0 based on given value
	cur_frm.set_value(field_name,value)
}

// function that sets custom buttons
function add_custom_buttons(button_name,action){
	cur_frm.add_custom_button(__(button_name), function(){
		//check cur_doc is new
		if(cur_frm.doc.__islocal){
			//throw an error to the customer
			frappe.throw("You need to save the document before running any action")
		}else{
			if(action=="view_customer_account"){
				//redirect to customer account document
				frappe.set_route('Form', 'Customer Account', cur_frm.doc.linked_customer_account)
			}else if(action=="view_customer"){
				//redirect to customer document
				frappe.set_route('Form', 'Customer', cur_frm.doc.customer)
			}
		}
	});
}

//function that filter fields
function filter_field(){
	//filter billing area field
    cur_frm.set_query("billing_area", function() {
		return {
		filters: {
				is_group: 0
			}
		};   
    });
}

var list_of_section_fields = {
	'billing_area':[
		'billing_area_1','billing_area_2','billing_area_3',
		'billing_area_4','billing_area_5','billing_area_6','billing_area_7',
		'billing_area_8','billing_area_9','billing_area_10'
	],
	'connection_details':[
		'meter','meter_installation_date',
		'meter_reading_on_installation'
	],
	'santitation_details':[
		'onsite','none','septic',
		'pit_latrine','traditional_pit_latrine',
		'pit_latrine_with_slab',
		'ventilated_improved_pit_latrine',
		'composing_inlet','individual_pit_latrine',
		'shared_pit_latrine','pour_flush_toilet_to_septic_tank',
		'pour_flush_toilet_to_septic_tank',
		'flush_toilet_to_septic_tank','individual_septic',
		'shared_septic','septic_tank_accessible_yes',
		'septic_tank_accessible_no'
	],
	'gps_coordinates_section':[
		'gps_cordinates','gps_coordinate_of_the_meter_x',
		'gps_coordinate_of_the_t_junction_y','x','y',
		'latitude','longitude','altitude','accuracy',
	],
	'map_section_section':[
		'map_location'
	]
}


//function tha make a list of given fields readable or readonly
//depending on the status
function make_fields_read_only(listOfFields,status){
	//billing area section
	listOfFields.forEach(field => {
		cur_frm.set_df_property(field,"read_only",status)
	});
	
}

//function that determines fields readbale and readonly list
function determine_read_only_fields(){
	var readOnlyList = []
	var readAbleList = []
	var section_fields = []

	//billing_area section
	if(cur_frm.doc.billing_area_confirmation == "Confirmed"){
		section_fields = list_of_section_fields.billing_area
		readOnlyList.push.apply(readOnlyList,section_fields)
	}else{
		section_fields = list_of_section_fields.billing_area
		readAbleList.push.apply(readAbleList,section_fields)
	}
	//connection details
	if(cur_frm.doc.meter_status == "Connected"){
		section_fields = list_of_section_fields.connection_details
		readOnlyList.push.apply(readOnlyList,section_fields)
	}else{
		if(cur_frm.doc.disconnection_level == 1 || cur_frm.doc.disconnection_level == 2){
			section_fields = list_of_section_fields.connection_details
			readOnlyList.push.apply(readOnlyList,section_fields)
		}else{
			section_fields = list_of_section_fields.connection_details
			readAbleList.push.apply(readAbleList,section_fields)
		}
	}

	//sanitation details section
	if(cur_frm.doc.sanitation_details_confirmation == "Confirmed"){
		section_fields = list_of_section_fields.santitation_details
		readOnlyList.push.apply(readOnlyList,section_fields)
	}else{
		section_fields = list_of_section_fields.santitation_details
		readAbleList.push.apply(readAbleList,section_fields)
	}

	//gps coordinates details section
	if(cur_frm.doc.gps_coordinates_confirmed == "Confirmed"){
		section_fields = list_of_section_fields.gps_coordinates_section
		readOnlyList.push.apply(readOnlyList,section_fields)
	}else{
		section_fields = list_of_section_fields.gps_coordinates_section
		readAbleList.push.apply(readAbleList,section_fields)
	}

	//make list readble and readonly
	make_fields_read_only(readOnlyList,1)
	make_fields_read_only(readAbleList,0)
}

//function that gets the current date
function todaysDate(){
	let today = new Date()
	return today.getFullYear()+'-'+(today.getMonth() + 1)+'-'+today.getDate()
}

frappe.ui.form.on('Customer Details', {
	refresh: function(frm) {
		//add custom buttons
		add_custom_buttons("View Customer Account","view_customer_account");
		add_custom_buttons("View Customer","view_customer");
		//filter field
		filter_field()
		//filter billing area fields
		filter_fields("billing_area_1",true)
		//make fields readonly
		determine_read_only_fields()
	}
});

//************************************************************************************************************
//billing area section
frappe.ui.form.on("Customer Details", "confirm_billing_area", function(frm){
	cur_frm.set_value("billing_area_confirmation","Confirmed")
	cur_frm.set_value("billing_area_transitioning",1)
	cur_frm.save()
});

frappe.ui.form.on("Customer Details", "unconfirm_billing_area", function(frm){
	cur_frm.set_value("billing_area_confirmation","Unconfirmed");
	cur_frm.set_value("billing_area_transitioning",1);
	cur_frm.save()
});

//************************************************************************************************************
//connection details section
//billing area section
frappe.ui.form.on("Customer Details", "mark_as_connected", function(frm){
	cur_frm.set_value("meter_status","Connected")
	cur_frm.set_value("connection_details_transitioning",1)
	cur_frm.set_value("disconnection_level",1)
	cur_frm.save()
});

frappe.ui.form.on("Customer Details", "mark_as_disconnected", function(frm){
	cur_frm.set_value("meter_status","Disconnected");
	cur_frm.set_value("connection_details_transitioning",1);
	cur_frm.set_value("disconnection_level",2)
	cur_frm.set_value("disconnection_date",todaysDate())
	cur_frm.save()
});

frappe.ui.form.on("Customer Details", "mark_as_permanently_disconnected", function(frm){
	if(cur_frm.doc.meter_status == "Disconnected" && cur_frm.doc.meter 
	&& cur_frm.doc.meter_installation_date  && 
	cur_frm.doc.meter_reading_on_installation){
		cur_frm.set_value("meter_status","Disconnected");
		cur_frm.set_value("connection_details_transitioning",1);
		cur_frm.set_value("disconnection_level",3)
		cur_frm.set_value("permanent_disconnection_date",todaysDate())
		cur_frm.save()
	}else{
		frappe.throw("Permanent Disconnection only apply to previousy connected accounts")
	}
});

//billing area 1
frappe.ui.form.on("Customer Details", "billing_area_1", function(frm){
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
frappe.ui.form.on("Customer Details", "billing_area_2", function(frm){
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
frappe.ui.form.on("Customer Details", "billing_area_3", function(frm){
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
frappe.ui.form.on("Customer Details", "billing_area_4", function(frm){
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
frappe.ui.form.on("Customer Details", "billing_area_5", function(frm){
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
frappe.ui.form.on("Customer Details", "billing_area_6", function(frm){
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
frappe.ui.form.on("Customer Details", "billing_area_7", function(frm){
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
frappe.ui.form.on("Customer Details", "billing_area_8", function(frm){
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
frappe.ui.form.on("Customer Details", "billing_area_9", function(frm){
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
frappe.ui.form.on("Customer Details", "billing_area_10", function(frm){
	//set as current billing area
	if(cur_frm.doc.billing_area_10){
		cur_frm.set_value("billing_area",cur_frm.doc.billing_area_10)
	}else{
		cur_frm.set_value("billing_area",cur_frm.doc.billing_area_9)
	}
});

//************************************************************************************************************
//sanitation details section

frappe.ui.form.on("Customer Details", "onsite", function(frm){
	//check if user clicked
	if(cur_frm.doc.onsite){
		clear_field("none",0)
	}
});

frappe.ui.form.on("Customer Details", "none", function(frm){
	//check if user clicked
	if(cur_frm.doc.none){
		clear_field("onsite",0)
	}
});


frappe.ui.form.on("Customer Details", "septic", function(frm){
	//check if user clicked
	if(cur_frm.doc.septic){
		clear_field("pit_latrine",0)
	}
});

frappe.ui.form.on("Customer Details", "pit_latrine", function(frm){
	//check if user clicked
	if(cur_frm.doc.pit_latrine){
		clear_field("septic",0)
	}
});

//triggered by confirm_sanitation_details
frappe.ui.form.on("Customer Details", "confirm_sanitation_details", function(frm){
	cur_frm.set_value("sanitation_details_confirmation","Confirmed")
	cur_frm.set_value("sanitation_details_transitioning",1)
	cur_frm.save()
});

//triggered by unconfirm_sanitation_details
frappe.ui.form.on("Customer Details", "unconfirm_sanitation_details", function(frm){
	cur_frm.set_value("sanitation_details_confirmation","Unconfirmed")
	cur_frm.set_value("sanitation_details_transitioning",1)
	cur_frm.save()
});

//************************************************************************************************************
//gps cordinates details section
//triggered by confirm_sanitation_details
frappe.ui.form.on("Customer Details", "confirm_coordinates", function(frm){
	cur_frm.set_value("gps_coordinates_confirmed","Confirmed")
	cur_frm.set_value("gps_coordinates_details_transitioning",1)
	cur_frm.save()
});

//triggered by unconfirm_sanitation_details
frappe.ui.form.on("Customer Details", "unconfirm_coordinates", function(frm){
	cur_frm.set_value("gps_coordinates_confirmed","Unconfirmed")
	cur_frm.set_value("gps_coordinates_details_transitioning",1)
	cur_frm.save()
});