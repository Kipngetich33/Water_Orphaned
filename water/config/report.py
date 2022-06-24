from __future__ import unicode_literals
from frappe import _
import frappe


def get_data():
	config = [
		{
			"label": _("Custom Reports"),
			"items": [
				{
					"type": "doctype",
					"name": "Leakage",
					"description": _("Leakage"),
					"onboard": 1,
				},
			]
        },
		{
			"label": _("Settings and Logs"),
			"items": [
				{
					"type": "doctype",
					"name": "Report Settings",
					"description": _("Report Settings"),
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
