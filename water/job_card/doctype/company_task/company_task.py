# -*- coding: utf-8 -*-
# Copyright (c) 2021, Upande LTD. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
#from typing_extensions import Required
import frappe
from frappe.model.document import Document

#python std lib import
import datetime

#app imports
from ....custom_methods.reusable_methods import create_single_company_task,create_child_company_tasks

class CompanyTask(Document):
	def validate(self):
		'''
		Function that validates the Company Task 
		document
		'''
		#check if name is given
		if not self.task_name:
			#check if task is created from common tasks
			if not self.created_from_common_tasks:
				frappe.throw("Field Task Name is required")

		#if the task is created_from_common_tasks
		if self.created_from_common_tasks:
			#then the field common_task cannot be empty since
			#it is required in the creation of tasks
			if not self.common_task:
				frappe.throw("If Task is created from common tasks\
					then the Common Task field cannot be empty")

	def before_save(self):
		'''
		Function that runs before the Company Task
		document is saved
		'''
		#check or create tasks
		if self.created_from_common_tasks:
			#check if the tasks have been added to child table
			if self.tasks_created:
				pass
			else:
				#get child tasks from the linked common task
				linked_common_task = frappe.get_doc('Common Tasks',self.common_task)
				create_child_company_tasks(self,linked_common_task)

		if self.is_group:
			#update values of child task
			self.child_task_value()
			#calculated completion percent and turnaround 
			#time
			total_tasks = 0
			closed_tasks = 0 
			turnaround_time = 0
			#loop through the given 
			for task in self.company_task_detail:
				if task.status == "Open":
					total_tasks += 1
					turnaround_time += task.turnaround_estimate_in_days
				elif task.status == "Closed":
					total_tasks += 1
					closed_tasks += 1
					turnaround_time += task.turnaround_estimate_in_days

			#completion percent
			completion_percent = closed_tasks/total_tasks * 100
			#set completion percent as status
			if completion_percent:
				if completion_percent == 100:
					self.status = "Closed"
				else:
					self.status = str(completion_percent)+"% Complete"
			else:
				self.status = "Open"

			#update turnaround time
			if turnaround_time:
				self.estimate_turnaround_time_in_days = turnaround_time
		
		#add start date
		if not self.start_date:			
			self.start_date = datetime.date.today()
		#add due date
		if not self.due_date:
			if self.estimate_turnaround_time_in_days:
				#round off to nearest whole number
				estimate_commpletion_time = round(self.estimate_turnaround_time_in_days)
				self.due_date = datetime.date.today() + datetime.timedelta(days=estimate_commpletion_time)

	def on_update(self):
		'''
		Function that runs once the document has been saved
		'''
		#check if task is not group
		if self.is_group == 0:
			#check if the task is linked to any group task
			child_task_list = frappe.get_list('Company Task Detail', filters = {
							'task_name': self.name
							},fields = ['name','parent']
						)

			#loop through each found child task
			for child_task in child_task_list:
				#get the parent of each child
				parent_task = frappe.get_doc("Company Task",child_task['parent'])
				parent_task.save(ignore_permissions = True)

	def child_task_value(self):
		'''
		Functiont that updates the values of the child
		tasks
		'''
		for child_task in self.company_task_detail:
			#get document of the linked child task
			linked_company_task = frappe.get_doc("Company Task",child_task.task_name)
			#now update all values
			child_task.status = linked_company_task.status
			child_task.title = linked_company_task.task_name
			#child_task.assigned_to = linked_company_task.status
			#child_task.assigned_by = linked_company_task.status
			child_task.turnaround_estimate_in_days = linked_company_task.estimate_turnaround_time_in_days
			child_task.description = linked_company_task.description
			

			

				





				
				


