# Copyright (c) 2024, Aadhil and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _

class Policy(Document):
    def validate(self):
        if self.premium_amount < 0:
            frappe.throw(_("Premium Amount cannot be negative."))

        if self.insurance_company and self.type_of_cover and not self.edit_commission_rate:
            if not self.commission_percentage:
                cp = get_commission_percentage_value(self.insurance_company, self.type_of_cover)
                if cp:
                    self.commission_percentage = cp
                else:
                    frappe.throw(_("No commission percentage found for the selected Insurance Company and Type of Cover"))

            self.commission_amount = (self.premium_amount * self.commission_percentage) / 100

@frappe.whitelist()
def get_commission_percentage(insurance_company, type_of_cover):
    if not (insurance_company and type_of_cover):
        return {"commission_percentage": 0}

    commission_percentage = frappe.db.get_value(
        "Insurance Type Details",
        {"parent": insurance_company, "type_of_cover": type_of_cover},
        "commission_percentage"
    )

    if commission_percentage is None:
        return {"commission_percentage": 0}
    
    return {"commission_percentage": commission_percentage}

def get_commission_percentage_value(insurance_company, type_of_cover):
    return frappe.db.get_value(
        "Insurance Type Details",
        {"parent": insurance_company, "type_of_cover": type_of_cover},
        "commission_percentage"
    )

