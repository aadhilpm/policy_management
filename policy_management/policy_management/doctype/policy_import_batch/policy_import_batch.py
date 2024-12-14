# Copyright (c) 2024, Aadhil and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.file_manager import get_file_path
import csv
import io
from frappe import _

class PolicyImportBatch(Document):
    pass

@frappe.whitelist()
def import_policies(docname):
    doc = frappe.get_doc("Policy Import Batch", docname)
    if not doc.file:
        return _("No file attached.")

    doc.import_status = "In Progress"
    doc.log = ""
    doc.save()

    file_path = get_file_path(doc.file)
    if not file_path:
        doc.import_status = "Error"
        doc.log = "File not found."
        doc.save()
        return _("File not found.")

    # Read CSV content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            csv_content = f.read()
    except Exception as e:
        doc.import_status = "Error"
        doc.log = f"Error reading file: {e}"
        doc.save()
        return _("Error reading file. Check logs.")

    reader = csv.DictReader(io.StringIO(csv_content))

    required_columns = ["policy_number", "start_date", "end_date", "name_of_insured", "mobile", "premium_amount", "make_and_type"]
    for col in required_columns:
        if col not in reader.fieldnames:
            doc.import_status = "Error"
            doc.log = f"Missing required column: {col}"
            doc.save()
            return _("CSV missing required columns: {0}").format(col)

    created_count = 0
    errors = []

    for row in reader:
        policy_data = {
            "doctype": "Policy",
            "policy_number": row.get("policy_number"),
            "start_date": row.get("start_date"),
            "end_date": row.get("end_date"),
            "name_of_insured": row.get("name_of_insured"),
            "mobile": row.get("mobile"),
            "premium_amount": row.get("premium_amount"),
            "insurance_company": doc.insurance_company,
            "type_of_cover": doc.type_of_cover,
            "make_and_type": row.get("make_and_type"),
            "status": row.get("status", "Active"),
            "email": row.get("email"),
            "qid": row.get("qid"),
            "year_of_manufacturer": row.get("year_of_manufacturer"),
            "registration_no": row.get("registration_no"),
            "commission_percentage": row.get("commission_percentage") or 0,
            "edit_commission_rate": int(row.get("edit_commission_rate") or 0)
        }

        try:
            validate_policy_data(policy_data)

            policy_doc = frappe.get_doc(policy_data)
            policy_doc.insert(ignore_permissions=True)
            created_count += 1

        except Exception as e:
            errors.append(f"Policy Number {row.get('policy_number')}: {e}")

    frappe.db.commit()

    if errors:
        doc.import_status = "Completed with Errors"
        doc.log = f"Created: {created_count}\nErrors:\n" + "\n".join(errors)
    else:
        doc.import_status = "Completed"
        doc.log = f"Created {created_count} policies successfully."

    doc.save()
    return doc.log

def validate_policy_data(data):
    from frappe.utils import validate_email_address
    if data.get("email"):
        validate_email_address(data["email"], True)

    if data.get("premium_amount") and not is_float(data["premium_amount"]):
        raise ValueError("Premium Amount must be a number")

    # Validate required date formats (start_date, end_date) if needed
    # Other validations as needed

def is_float(value):
    try:
        float(value)
        return True
    except:
        return False
