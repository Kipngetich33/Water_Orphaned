from __future__ import unicode_literals
from frappe import _
import frappe


def get_data():
	config = [
		{
			"label": _("Meter Reading"),
			"items": [
				{
					"type": "doctype",
					"name": "Meter",
					"description": _("Meter"),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Meter Reading",
					"description": _("Meter Reading"),
					"onboard": 1,
				},
                {
					"type": "doctype",
					"name": "Meter Reading Sheet",
					"description": _("Meter Reading Sheet"),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Meter Reader Routes",
					"description": _("Meter Reader Routes"),
					"onboard": 1,
				}
			]
        },
		{
			"label": _("Settings and Logs"),
			"items": [
				{
					"type": "doctype",
					"name": "Meter Reading Settings",
					"description": _("Meter Reading Settings"),
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
