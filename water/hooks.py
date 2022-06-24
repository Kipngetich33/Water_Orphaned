# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "water"
app_title = "Water"
app_publisher = "Upande LTD."
app_description = "application for water utilities"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "dev@upande.com"
app_license = "Proprietary"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/water/css/water.css"
# app_include_js = "/assets/water/js/water.js"

# include js, css files in header of web template
# web_include_css = "/assets/water/css/water.css"
# web_include_js = "/assets/water/js/water.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "water.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "water.install.before_install"
# after_install = "water.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "water.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Sales Invoice": {
		#"on_update": "water.custom_methods.billing_methods.test",
		#"on_submit": "water.custom_methods.billing_methods.test2",
		"on_cancel": "water.custom_methods.billing_methods.check_invoice_cancellation",
		# "on_trash": "method"
	},
	"Payment Entry": {
		# "before_save":"water.custom_methods.billing_methods.test",
		# "on_update": "water.custom_methods.billing_methods.payment_submission",
		"on_submit": "water.custom_methods.billing_methods.payment_submission",
		# "on_cancel": "water.custom_methods.billing_methods.payment_submission",
		# "on_trash": "method"
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	# "cron":{
	# 	"* * * * *":[
	# 		"water.tasks.cron"
	# 	]
	# },
	# "all": [
# 		"water.tasks.all"
# 	],
# 	"daily": [
# 		"water.tasks.daily"
# 	],
	"hourly": [
	    "water.cis.cis_custom_methods.fetch_cis_from_ona",
		"water.custom_methods.leakage_methods.fetch_leakage_from_ona"
	],
# 	"weekly": [
# 		"water.tasks.weekly"
# 	]
# 	"monthly": [
# 		"water.tasks.monthly"
# 	]
}

# Testing
# -------

# before_tests = "water.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "water.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "water.task.get_dashboard_data"
# }

