# -*- coding: utf-8 -*-


{
    'name': "Sale To MIS Reporting(SO & PO)",
    'summary': """ Create and Update MIS from Sale """,
    'description': """
This allow you to create/update MIS Reporting from Sale
    """,
    'author': "Rajeev Kumar.",
    'website': "",
    'images': [],
    'version': '1.0',
    'category' : 'sale',
    'depends': ['base','sale', 'purchase',],
    'data':[
        'views/so_to_mis_view.xml',
		#'Security/ir.model.access.csv',
    ],
    'installable' : True,
    'application' : False,
    'auto_install' : False,
}
