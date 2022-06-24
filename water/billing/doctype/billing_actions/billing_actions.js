// Copyright (c) 2021, Upande LTD. and contributors
// For license information, please see license.txt
function filter_meter_reading_sheets(){
	cur_frm.set_query('meter_reading_sheet', function() {
		return {
			"filters": {
				"status": "Closed",
				"billed": 0
			}
		}
	})
}

frappe.ui.form.on('Billing Actions', {
	refresh: function(frm) {
		//call the meter reading sheet filter
		filter_meter_reading_sheets()
	}
});

//function that runs when the bill_selected_sheet is clicked
frappe.ui.form.on('Billing Actions','bill_selected_sheet', function(frm){
	//mark billing_the_sheet as True
	cur_frm.set_value('billing_the_sheet',1)
	//now save the document
	cur_frm.save()
})