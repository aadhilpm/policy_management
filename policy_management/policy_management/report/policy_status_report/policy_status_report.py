# Copyright (c) 2024, Aadhil and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import today, date_diff, add_days

def execute(filters=None):
    if not filters:
        filters = {}

    data = get_data(filters)
    
    columns = get_columns()
    
    return columns, data

def get_columns():
    return [
        {
            "fieldname": "policy_number",
            "label": "Policy Number",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "name_of_insured",
            "label": "Name of Insured",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "fieldname": "start_date",
            "label": "Start Date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "fieldname": "end_date",
            "label": "End Date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "fieldname": "days_to_expire",
            "label": "Days to Expire",
            "fieldtype": "Int",
            "width": 120
        },
        {
            "fieldname": "status",
            "label": "Status",
            "fieldtype": "Select",
            "width": 100
        },
        {
            "fieldname": "insurance_company",
            "label": "Insurance Company",
            "fieldtype": "Link",
            "options": "Insurance Company",
            "width": 200
        },
        {
            "fieldname": "type_of_cover",
            "label": "Type of Cover",
            "fieldtype": "Link",
            "options": "Type of Cover",
            "width": 150
        },
        {
            "fieldname": "premium_amount",
            "label": "Premium Amount",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "mobile",
            "label": "Mobile",
            "fieldtype": "Phone",
            "width": 160
        }
    ]

def get_data(filters):
    conditions = []

    if filters.get("status"):
        conditions.append("status = %(status)s")
    
    if filters.get("end_date"):
        conditions.append("end_date <= %(end_date)s")
    
    if filters.get("start_date"):
        conditions.append("end_date >= %(start_date)s")
    
    if filters.get("insurance_company"):
        conditions.append("insurance_company = %(insurance_company)s")
    
    if filters.get("type_of_cover"):
        conditions.append("type_of_cover = %(type_of_cover)s")
    
    if filters.get("days_to_expire"):
        days_to_expire_filter = add_days(today(), filters["days_to_expire"])
        conditions.append("end_date <= %(days_to_expire_filter)s")
        filters["days_to_expire_filter"] = days_to_expire_filter
    
    where_clause = " AND ".join(conditions) if conditions else "1=1"
    
    query = f"""
        SELECT
            policy_number,
            name_of_insured,
            start_date,
            end_date,
            status,
            insurance_company,
            type_of_cover,
            premium_amount,
            mobile
        FROM
            `tabPolicy`
        WHERE
            {where_clause}
        ORDER BY
            end_date ASC
    """

    policies = frappe.db.sql(query, filters, as_dict=True)
    
    today_date = today()
    for policy in policies:
        days_to_expire = date_diff(policy.get("end_date"), today_date)
        policy["days_to_expire"] = days_to_expire

    return policies

