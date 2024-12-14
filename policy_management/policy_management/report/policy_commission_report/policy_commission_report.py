# Copyright (c) 2024, Aadhil and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Policy Name", "fieldname": "name", "fieldtype": "Link", "options": "Policy", "width": 150},
        {"label": "Insurance Company", "fieldname": "insurance_company", "fieldtype": "Link", "options": "Insurance Company", "width": 200},
        {"label": "Type of Cover", "fieldname": "type_of_cover", "fieldtype": "Data", "width": 150},
        {"label": "Premium Amount", "fieldname": "premium_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Commission Percentage", "fieldname": "commission_percentage", "fieldtype": "Percent", "width": 150},
        {"label": "Commission Amount", "fieldname": "commission_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Creation Date", "fieldname": "creation", "fieldtype": "Date", "width": 150},
    ]

def get_data(filters):
    query = """
        SELECT
            name,
            insurance_company,
            type_of_cover,
            premium_amount,
            commission_percentage,
            commission_amount,
            creation
        FROM
            `tabPolicy`
        WHERE
            docstatus < 2
    """

    if filters.get("from_date"):
        query += " AND creation >= %(from_date)s"
    if filters.get("to_date"):
        query += " AND creation <= %(to_date)s"
    if filters.get("insurance_company"):
        query += " AND insurance_company = %(insurance_company)s"
    if filters.get("type_of_cover"):
        query += " AND type_of_cover = %(type_of_cover)s"

    return frappe.db.sql(query, filters, as_dict=True)
