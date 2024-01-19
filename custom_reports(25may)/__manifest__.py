# -*- coding: utf-8 -*-
{
    'name' : 'Custom Reports',
    'version' : '1.1',
    'summary': 'Send Invoices and Track Payments',
    'sequence': 30,
	'author': "Rajeev Kumar.",
    'description': """ Creates Custom report for invoices and packing list """,
	'category': 'Accounting',
	'depends' : ['base', 'account', 'analytic', 'report', 'web_planner'],
	'data': [ 'views/reports.xml','templates/packing_list.xml',
		'templates/commercial_invoice.xml'
	],
	'installable': True,
    'application': True,
    'auto_install': False,
}
