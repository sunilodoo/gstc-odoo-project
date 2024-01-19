# -*- coding: utf-8 -*-
{
    'name': 'Purchase Reports Excel',
    'version': '1.0.0',
    'category': 'Purchase',
    'summary': '''
        Prints Excel Report based on Purchase By Products to Buyar.
        ''',
    'author': 'Santosh Singh',
    'license': "",
    'depends': [
        'base','web','sale','purchase','website',
    ],
    'data': [
		'security/ir.model.access.csv',
        'wizard/purchase_report_xls_view.xml'
    ],
    'demo': [],  
    'auto_install': False,
    'installable': True,
    'application': True
}
