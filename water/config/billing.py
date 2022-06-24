from __future__ import unicode_literals
from frappe import _
import frappe

def get_data():
	return [
		{
			"label": _("Customer Management & Billing"),
			"items": [
				{
					"type": "doctype",
					"name": "Customer Account",
					"description": _("Customer Account"),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Customer Details",
					"description": _("Customer Details"),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Customer Type",
					"description": _("Customer Type"),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Billing Area",
					"description": _("Billing Area"),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Billing Period",
					"description": _("Billing Period"),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Bill Item",
					"description": _("Bill Item"),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Bill",
					"description": _("Bill"),
					"onboard": 1,
				},
			]
        },
		{
			"label": _("Settings and Logs"),
			"items": [
				{
					"type": "doctype",
					"name": "Billing Settings",
					"description": _("Billing Settings"),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Billing Settings Item",
					"description": _("Billing Settings Item"),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "System Error Log",
					"description": _("System Error Log"),
					"onboard": 1,
				}
			]
        },
		{
			"label": _("Actions"),
			"items": [
				{
					"type": "doctype",
					"name": "Billing Actions",
					"description": _("Billing Actions"),
					"onboard": 1,
				}
			]
        },
		
    ]