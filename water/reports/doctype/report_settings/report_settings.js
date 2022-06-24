// Copyright (c) 2021, Upande LTD. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Report Settings', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on("Report Settings", "fetch_leakages_now", function (frm) {
	//call report settings
	frappe.call({
		method: "water.reports.custom_report_methods.leakage_methods.fetch_leakage_from_ona",
		callback: function(response) {
			if(response.message.status){
				//throw message
				frappe.msgprint({
					title: __('Complete!'),
					indicator: 'green',
					message: __('New Leakage entries fetched successfully')
				});
			}else{
				//throw message
				frappe.msgprint({
					title: __('Error!'),
					indicator: 'red',
					message: __('Error occured fetching entries, please check System \
						Error logs for details')
				});
			}
		}
	});
});