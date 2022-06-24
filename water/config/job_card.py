from __future__ import unicode_literals
from frappe import _
import frappe


def get_data():
	config = [
		{
			"label": _("Job Card"),
			"items": [
				{
					"type": "doctype",
					"name": "Company Task",
					"description": _("Company Task"),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Common Tasks",
					"description": _("Common Tasks"),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Common Task Detail",
					"description": _("Common Task Detail"),
					"onboard": 1,
				},
				
			]
        },
		{
			"label": _("Settings and Logs"),
			"items": [
				{
					"type": "doctype",
					"name": "Job Card Setting",
					"description": _("Job Card Setting"),
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
