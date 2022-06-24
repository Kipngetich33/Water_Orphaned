// Copyright (c) 2021, Upande LTD. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Billing Settings', {
	// refresh: function(frm) {

	// }
});

//function that runs when the bill_selected_sheet is clicked
frappe.ui.form.on('Billing Settings','create_geolocation_field', function(frm){
	frappe.msgprint(`Creating a Geometry field in the ${cur_frm.doc.reference_doctype} doctype`)
	//validate the action
	let validationStatus = validateAdditionOfGeomField()
	if(validationStatus.status){
		//call the add Geolocation field
		callFunctToAddGeomField()
	}else{
		frappe.msgprint(validationStatus.message)
	}
})

function validateAdditionOfGeomField(){
	//check if target doctype is defined
	if(cur_frm.doc.reference_doctype){
		//check if default Geolocation is defined
		if(cur_frm.doc.default_geolocation_field){
			return {'status':true}
		}else{
			return {
				'status':false,
				'message':"You have not defined the default Geolocation Point"
			}
		}
	}else{
		return {
			'status':false,
			'message':"You have not selected the Target Doctype"
		}
	}
}

function callFunctToAddGeomField(){
	frappe.call({
        method: "water.utils.add_spatial_field_to_doctype",
        args: {
			target_doctype:cur_frm.doc.reference_doctype,
			geometry_field:"geometry_field",
			geolocation_value:cur_frm.doc.default_geolocation_field
		},
        callback: function(r) {
			if(r.message.status){
				//alert a success message
				frappe.msgprint(`Successfully added a Geometry field to the \
				${cur_frm.doc.reference_doctype} doctype`)
				//clear the doctype field
				cur_frm.set_value("reference_doctype","")
			}else if(r.message.status == false){
				frappe.msgprint(r.message.message)
			}
        }
	});
}