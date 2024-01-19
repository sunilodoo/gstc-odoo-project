# -*- coding: utf-8 -*-


{
    'name': "PO Item-wise History",
    'summary': """ PO Item-wise History """,
    'description': """
PO Item-wise History
    """,
    'author': "Rajeev Kumar.",
    'website': "",
    'images': [],
    'version': '1.0',
    'category' : 'custom',
    'depends': ['base','purchase', 'account','stock', 'delivery'],
    'data':[
        'views/po_item_history_view.xml',
		'views/template.xml',
		'Security/ir.model.access.csv',
    ],
    'installable' : True,
    'application' : False,
    'auto_install' : False,
}
