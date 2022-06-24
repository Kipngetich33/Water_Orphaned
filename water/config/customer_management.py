from __future__ import unicode_literals
from frappe import _
import frappe


def get_data():
	config = [
		{
			"label": _("Customer Management"),
			"items": [
				{
					"type": "doctype",
					"name": "CIS Data",
					"description": _("CIS Data"),
					"onboard": 1,
				},
                {
					"type": "doctype",
					"name": "CIS Project",
					"description": _("CIS Project"),
					"onboard": 1,
				},
				{
					"type": "page",
					"name": "data-analysis",
					"description": _("Data Analysis"),
					"onboard": 1,
				},
			]
        },
		{
			"label": _("Settings and Logs"),
			"items": [
				{
					"type": "doctype",
					"name": "CIS Settings",
					"description": _("CIS Settings"),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "System Error Log",
					"description": _("System Error Log"),
					"onboard": 1,
				}
				
			]
        }
    ]
	return config
