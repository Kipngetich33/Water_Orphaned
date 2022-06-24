# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "Billing",
			"color": "grey",
			"icon": "octicon octicon-tag",
			"type": "module",
			"label": _("Billing")
		},
		{
			"module_name": "CIS",
			"color": "grey",
			"icon": "octicon octicon-database",
			"type": "module",
			"label": _("CIS")
		},
		{
			"module_name": "Job Card",
			"color": "grey",
			"icon": "octicon octicon-checklist",
			"type": "module",
			"label": _("Job Card")
		},
		{
			"module_name": "Meter Reading",
			"color": "grey",
			"icon": "octicon octicon-credit-card",
			"type": "module",
			"label": _("Meter Reading")
		},
		{
			"module_name": "Report",
			"color": "grey",
			"icon": "octicon octicon-graph",
			"type": "module",
			"label": _("Report")
		}
	]
