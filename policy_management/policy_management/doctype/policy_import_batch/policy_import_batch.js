// Copyright (c) 2024, Aadhil and contributors
// For license information, please see license.txt

frappe.ui.form.on('Policy Import Batch', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('Import Policies'), () => {
                frappe.call({
                    method: "policy_management.policy_management.doctype.policy_import_batch.policy_import_batch.import_policies",
                    args: {
                        docname: frm.doc.name
                    },
                    freeze: true,
                    freeze_message: __("Importing Policies..."),
                    callback: function(r) {
                        if (r.message) {
                            frappe.msgprint(r.message);
                            frm.reload_doc();
                        }
                    }
                });
            });
        }
    }
});
