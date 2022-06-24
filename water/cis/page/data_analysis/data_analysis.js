frappe.pages['data-analysis'].on_page_load = function(wrapper) {
	// redirect to correct page
	redirectFunction()

	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Data Analysis',
		single_column: true
	});
}

function redirectFunction() {
	location.replace("/data_analysis")
}