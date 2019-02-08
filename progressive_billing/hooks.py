# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "progressive_billing"
app_title = "Progressive Billing"
app_publisher = "Craft"
app_description = "App for progressive billing"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "hafeesk@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/progressive_billing/css/progressive_billing.css"
# app_include_js = "/assets/progressive_billing/js/progressive_billing.js"

# include js, css files in header of web template
# web_include_css = "/assets/progressive_billing/css/progressive_billing.css"
# web_include_js = "/assets/progressive_billing/js/progressive_billing.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Sales Invoice" : "public/js/sales_invoice.js"}
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
# get_website_user_home_page = "progressive_billing.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "progressive_billing.install.before_install"
# after_install = "progressive_billing.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "progressive_billing.notifications.get_notification_config"

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


fixtures = [{"dt": "Custom Field", "filters":[["name", "in", ['Sales Invoice-progressive_billing','Sales Invoice-sales_order','Sales Invoice-project_progressive','Sales Invoice-get_items_from_task','Sales Invoice-get_items_from_payment_terms','Sales Invoice-column_break_22','Sales Invoice-sales_order_total','Sales Invoice-total_invoiced','Sales Invoice-pending_invoice_amount','Sales Invoice-column23223','Sales Invoice-total_due_now','Sales Invoice-new_invoiced_total','Sales Invoice-total_after_current_invoice','Task-rate','Sales Invoice Item-progress']]]}]


# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }
doc_events = {
	'Project': {
		'validate': 'progressive_billing.progressive_billing.progressive_billing.validate_app',
	}
}
# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"progressive_billing.tasks.all"
# 	],
# 	"daily": [
# 		"progressive_billing.tasks.daily"
# 	],
# 	"hourly": [
# 		"progressive_billing.tasks.hourly"
# 	],
# 	"weekly": [
# 		"progressive_billing.tasks.weekly"
# 	]
# 	"monthly": [
# 		"progressive_billing.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "progressive_billing.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "progressive_billing.event.get_events"
# }

