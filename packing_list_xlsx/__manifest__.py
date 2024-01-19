# -*- coding: utf-8 -*-
{
    'name' : 'Packing List Excel Report',
    'version': '10.0',
    'author': 'Rajeev Kumar',
    'category': 'Invoice',
    'website': '',
    'summary': 'Excel sheet for Packing List',
    'description': """ Excel sheet for Packing List""",
    'depends': [
        'base','sale','purchase','account'
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/packing_list_xls_view.xml',
    ],
    'images': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
