# -*- coding: utf-8 -*-
###################################################################################
{
    'name': 'Customer Report XLS & PDF',
    'version': '10.0.2.0.0',
    "category": "Tools",
    'author': 'Rajeev Kumar',
    'website': "",
    'company': '',
    'summary': """Advanced PDF & XLS Reports For Customers""",
    'depends': ['base', 'sale', 'purchase', 'report_xlsx'],
    'license': 'AGPL-3',
    'data': [
            'views/wizard_report.xml',
             'views/customer_report_pdf_view.xml',
             #'views/customer_report_button.xml',
             'views/customer_report.xml',
			 'Security/ir.model.access.csv',
             ],
    'images': [],
    'installable': True,
    'auto_install': False,
}
