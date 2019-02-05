frappe.ui.form.on('Sales Invoice', {	
	sales_order:function(frm){
                
		console.log(frm.doc)
                frappe.call({
                        method:"frappe.client.get_value",
                        args: {
                                doctype:"Project",
                                filters: {
                                        'sales_order':frm.doc.sales_order,
                                },
                                fieldname:["name","total_sales_amount","customer"]
                        },
                        async:false,
                        callback: function(r) {
				console.log(r)
       	                         // set the returned value in a field
                                frm.set_value('project_progressive', r.message.name);
                                frm.set_value('project', r.message.name);
                                frm.set_value('customer', r.message.customer.toString());
                                frm.set_value('sales_order_total', r.message.total_sales_amount);
                        }
                });

		frm.cscript.customer();
                frappe.call({
                                method: "progressive_billing.progressive_billing.progressive_billing.get_progressive_invoice_data",
                                args: {
                                        "sales_order": frm.doc.sales_order,
                                        "project": frm.doc.project

                                },
                                callback: function (r) {

                                        frm.set_value('total_invoiced',r.message.total_invoiced);
                                        frm.set_value('total_due_now',r.message.outstanding_amount);
                                        frm.set_value('pending_invoice_amount',frm.doc.sales_order_total-r.message.total_invoiced);                                                 
					frm.set_value('new_invoiced_total',frm.doc.grand_total);
                                        frm.set_value('total_after_current_invoice',frm.doc.grand_total+r.message.total_invoiced);


                                }
                        });

  	 },
	 get_items_from_task:function(frm){
                

                frappe.call({

                        method: "progressive_billing.progressive_billing.progressive_billing.get_item_data",
                        args: {
                                  "sales_order": frm.doc.sales_order,
                                  "project": frm.doc.project

                        },
                        callback: function(r) { 
                                
                                frm.doc.items=[]
                                for(i=0;i<r.message.length;i++){
                                        console.log(r.message[i])

                                        var child = frm.add_child("items");
                                        frappe.model.set_value(child.doctype, child.name, "description", r.message[i].subject)
                                        frappe.model.set_value(child.doctype, child.name, "item_name", r.message[i].subject)

                                        //frappe.model.set_value(child.doctype, child.name, "rate", r.message[i].rate)
                                        frappe.model.set_value(child.doctype, child.name, "qty", 1)
                                        frappe.model.set_value(child.doctype, child.name, "uom", r.message[i].uom)
                                        frappe.model.set_value(child.doctype, child.name, "sales_order", frm.doc.sales_order.toString())
                                        frappe.model.set_value(child.doctype, child.name, "conversion_factor", 1)
                                        frappe.model.set_value(child.doctype, child.name, "income_account", r.message[i].income_account)
                                        frappe.model.set_value(child.doctype, child.name, "progress", r.message[i].progress)
                                        frappe.model.set_value(child.doctype, child.name, "rate", (r.message[i].rate*r.message[i].progress)/100)
                                }

                                frm.refresh_field('items');

                        } 
                });


        },

	  
})
