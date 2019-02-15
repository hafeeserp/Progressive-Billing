from __future__ import unicode_literals
import frappe, erpnext
import frappe.defaults
from frappe.utils import cint, flt
from frappe import _, msgprint, throw
from erpnext.accounts.party import get_party_account, get_due_date
from erpnext.controllers.stock_controller import update_gl_entries_after
from frappe.model.mapper import get_mapped_doc
from erpnext.accounts.doctype.sales_invoice.pos import update_multi_mode_option

from erpnext.controllers.selling_controller import SellingController
from erpnext.accounts.utils import get_account_currency
from erpnext.stock.doctype.delivery_note.delivery_note import update_billed_amount_based_on_so
from erpnext.projects.doctype.timesheet.timesheet import get_projectwise_timesheet_data
from erpnext.assets.doctype.asset.depreciation \
        import get_disposal_account_and_cost_center, get_gl_entries_on_asset_disposal
from erpnext.stock.doctype.batch.batch import set_batch_nos
from erpnext.stock.doctype.serial_no.serial_no import get_serial_nos, get_delivery_note_serial_no
from erpnext.setup.doctype.company.company import update_company_current_month_sales
from erpnext.accounts.general_ledger import get_round_off_account_and_cost_center
from erpnext import get_company_currency, get_default_company
from erpnext.projects.doctype.project.project import Project

@frappe.whitelist()
def get_progressive_invoice_data(sales_order='', project='',test=''):
        pgrsve_data = frappe.db.sql("""select sum(grand_total),sum(outstanding_amount) from `tabSales Invoice` where project_progressive=%s and sales_order=%s and docstatus=1""",(project,sales_order))[0]
        if pgrsve_data:
                return {'total_invoiced':pgrsve_data[0],'outstanding_amount':pgrsve_data[1]}
        else:
                return {'total_invoiced':0.00,'outstanding_amount':0.00}

@frappe.whitelist()
def get_item_data(sales_order='', project='',test=''):
        task_data = frappe.db.sql("""select subject,progress,rate,qty,item_amount,uom from `tabTask` where project=%s""",project)
        lst_item_data = []
	
        default_uom = frappe.db.get_single_value('Stock Settings','stock_uom')
        income_account = frappe.db.get_value('Company',get_default_company(),'default_income_account')
        for task in task_data:
                item_data = {}
		
		sales_invoices = frappe.db.sql("""select name from `tabSales Invoice` where sales_order=%s and docstatus = 1""",sales_order)
		invoice_list = []
		if sales_invoices:
			for invoice in sales_invoices:
				invoice_list.append(invoice[0])
		#frappe.msgprint(frappe.as_json(invoice_list))
                #total_progress = frappe.db.sql("""select sum(progress) from `tabSales Invoice Item` where parent in (%s) and item_name=%s and sales_order=%s""" %(', '.join(["%s"]*len(invoice_list))), tuple(invoice_list),'%s','%s'),)[0][0]
		#total_progress = frappe.db.sql("""select sum(progress) from `tabSales Invoice Item` where sales_order=%s and item_name=%s""",(sales_order,task[0]))[0][0]
		#items = list(set([d for d in invoice_list]))
		items = invoice_list
		if items:
			total_progress = frappe.db.sql("""select sum(progress) from `tabSales Invoice Item` where item_name=%s and sales_order=%s and parent in ({0})""".format(", ".join(["%s"] * len(items))), [task[0]] +[sales_order]+items)[0][0]
		else:
			total_progress = 0
                item_data['subject']=task[0]
                if total_progress:
                        item_data['current_progress']=task[1]
                        item_data['progress']=task[1]-total_progress
		
                else:
                        item_data['current_progress']=0
                        item_data['progress']=task[1]
		
                item_data['uom'] = task[5]
                item_data['income_account'] = income_account
                item_data['rate'] = task[2]
		item_data['item_rate'] = task[4]
		item_data['qty'] = task[3]
		
		
                lst_item_data.append(item_data)

        return tuple(lst_item_data)

@frappe.whitelist()
def make_project(source_name, target_doc=None):
	def postprocess(source, doc):
		doc.project_type = "External"
		doc.project_name = source.name

	doc = get_mapped_doc("Sales Order", source_name, {
		"Sales Order": {
			"doctype": "Project",
			"validation": {
				"docstatus": ["=", 1]
			},
			"field_map":{
				"name" : "sales_order",
				"base_grand_total" : "estimated_costing",
			}
		},
		"Sales Order Item": {
			"doctype": "Project Task",
			"field_map": {
				"item_name": "title",
				"qty":"qty",
				"amount":"rate",
				"rate":"item_amount",
				"uom":"uom"
			},
		}
	}, target_doc, postprocess)
	return doc


def validate_app(doc,method):
	Project.validate = validate

def validate(self):
	task_total = 0
	for task in self.tasks:
                task_total += task.rate
	self.validate_project_name()
        self.validate_dates()
        self.validate_weights()
	total_sales_amount = frappe.db.sql("""select grand_total from `tabSales Order` where name=%s""",self.sales_order)[0]

        if total_sales_amount:
                if task_total > total_sales_amount[0]:
                        frappe.throw(_("Task Total Can Not Be Greater Than Sales Order Amount"))

        self.sync_tasks()
        self.tasks = []
        self.send_welcome_email()
	'''total_sales_amount = frappe.db.sql("""select grand_total from `tabSales Order` where name=%s""",self.sales_order)[0]
	
	if total_sales_amount:
		if task_total > total_sales_amount[0]:
			frappe.throw(_("Task Total Can Not Be Greater Than Sales Order Amount"))'''
