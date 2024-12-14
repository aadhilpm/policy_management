frappe.ui.form.on('Policy', {
    insurance_company: function (frm) {
        if (frm.doc.insurance_company && frm.doc.type_of_cover && !frm.doc.edit_commission_rate) {
            fetch_commission_percentage(frm);
        }
    },
    type_of_cover: function (frm) {
        if (frm.doc.insurance_company && frm.doc.type_of_cover && !frm.doc.edit_commission_rate) {
            fetch_commission_percentage(frm);
        }
    },
    premium_amount: function (frm) {
        validate_premium_amount(frm);
        calculate_commission_amount(frm);
    },
    commission_percentage: function (frm) {
        calculate_commission_amount(frm);
    }
});

function fetch_commission_percentage(frm) {
    frappe.call({
        method: 'policy_management.policy_management.doctype.policy.policy.get_commission_percentage',
        args: {
            insurance_company: frm.doc.insurance_company,
            type_of_cover: frm.doc.type_of_cover
        },
        callback: function (r) {
            if (r.message) {
                frm.set_value('commission_percentage', r.message.commission_percentage || 0);
                calculate_commission_amount(frm);
            } else {
                frappe.msgprint(__('No commission percentage found for the selected Insurance Company and Type of Cover'));
                frm.set_value('commission_percentage', 0);
                frm.set_value('commission_amount', 0);
            }
        }
    });
}

function calculate_commission_amount(frm) {
    const commission_percentage = frm.doc.commission_percentage || 0;
    const premium_amount = frm.doc.premium_amount || 0;
    const commission_amount = (premium_amount * commission_percentage) / 100;
    frm.set_value('commission_amount', commission_amount);
}

function validate_premium_amount(frm) {
    if (frm.doc.premium_amount < 0) {
        frappe.msgprint(__('Premium Amount cannot be negative.'));
        frm.set_value('premium_amount', 0);
    }
}
