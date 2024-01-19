# -*- coding: utf-8 -*-
{
    'name' : 'Commercial Excel Report',
    'version': '10.0',
    'author': 'Rajeev Kumar',
    'category': 'Invoice',
    'website': '',
    'summary': 'Excel sheet for Commercial Invoice',
    'description': """ Excel sheet for Commercial Invoice""",
    'depends': [
        'base','sale','purchase','account'
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/commercial_invoice_xls_view.xml',
    ],
    'images': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
