// Copyright (c) 2024, Aadhil and contributors
// For license information, please see license.txt

frappe.query_reports["Policy Commission Report"] = {
    "filters": [
		{
            "fieldname": "from_date",
            "label": "From Date",
            "fieldtype": "Date",
            "default": "",
            "reqd": 0
        },
		{
            "fieldname": "to_date",
            "label": "To Date",
            "fieldtype": "Date",
            "default": "",
            "reqd": 0
        },
        {
            "fieldname": "insurance_company",
            "label": "Insurance Company",
            "fieldtype": "Link",
            "options": "Insurance Company",
            "default": "",
            "reqd": 0
        },
        {
            "fieldname": "type_of_cover",
            "label": "Type of Cover",
            "fieldtype": "Link",
			"options": "Type of Cover",
            "default": "",
            "reqd": 0
        }
    ]
}

