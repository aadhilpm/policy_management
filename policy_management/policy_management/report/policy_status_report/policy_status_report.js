// Copyright (c) 2024, Aadhil and contributors
// For license information, please see license.txt

frappe.query_reports["Policy Status Report"] = {
    filters: [
        {
            fieldname: "status",
            label: __("Status"),
            fieldtype: "Select",
            options: ["", "Active", "Expired"]
        },
        {
            fieldname: "insurance_company",
            label: __("Insurance Company"),
            fieldtype: "Link",
            options: "Insurance Company"
        },
        {
            fieldname: "type_of_cover",
            label: __("Type of Cover"),
            fieldtype: "Link",
            options: "Type of Cover"
        },
        {
            fieldname: "start_date",
            label: __("Start Date"),
            fieldtype: "Date",
        },
        {
            fieldname: "end_date",
            label: __("End Date"),
            fieldtype: "Date",
        },
        {
            fieldname: "days_to_expire",
            label: __("Days to Expire"),
            fieldtype: "Int",
            description: __("Enter the maximum number of days until the policy expires.")
        }
    ],

    // Add conditional formatting
    onload: function(report) {
        report.page.add_inner_button(__("Refresh"), function() {
            report.refresh();
        });
    },

    formatter: function(value, row, column, data, default_formatter) {
        if (!data) {
            return value;
        }

        let formatted_value = default_formatter(value, row, column, data);

        // Add color for 'status'
        if (column.fieldname === "status") {
            if (data.status === "Active") {
                formatted_value = `<span style="color: green; font-weight: bold;">${value}</span>`;
            } else if (data.status === "Expired") {
                formatted_value = `<span style="color: red; font-weight: bold;">${value}</span>`;
            }
        }

        // Add color for 'days_to_expire'
        if (column.fieldname === "days_to_expire") {
            if (data.days_to_expire <= 0) {
                formatted_value = `<span style="color: red; font-weight: bold;">${value}</span>`;
            } else if (data.days_to_expire <= 30) {
                formatted_value = `<span style="color: orange; font-weight: bold;">${value}</span>`;
            } else {
                formatted_value = `<span style="color: green; font-weight: bold;">${value}</span>`;
            }
        }

        return formatted_value;
    }
};
