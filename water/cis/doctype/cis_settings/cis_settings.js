// Copyright (c) 2021, Upande LTD. and contributors
// For license information, please see license.txt
frappe.ui.form.on('CIS Settings', {
	// refresh: function(frm) {

	// }
});

// functionality triggered clicking on the fetch_cis_data button
frappe.ui.form.on("CIS Settings", "fetch_cis_data", function (frm) {
	if(cur_frm.doc.fetching_cis_data_on){
		// set it to off
		cur_frm.set_value("fetching_cis_data_on",0)
		cur_frm.save()
		frappe.msgprint("Fetching of CIS Data from ONA turned OFF Successfully")
	}else{
		cur_frm.set_value("fetching_cis_data_on",1)
		cur_frm.save()
		frappe.msgprint("Fetching of CIS Data from ONA turned ON Successfully")
	}
});

// functionality triggered clicking on the fetch_new_entries button
frappe.ui.form.on("CIS Settings", "fetch_new_entries", function (frm) {
	frappe.msgprint("Fetching New Entries from Remote Sever")
	frappe.call({
        method: "water.cis.cis_custom_methods.fetch_cis_from_ona",
        args: {},
        callback: function(r) {
			if(r.message.status){
				frappe.msgprint("Fetching New Entries from Remote Sever Complete")
			}else if(r.message.status == false){
				frappe.msgprint(r.message.message)
			}
        }
	});
});
