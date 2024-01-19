# -*- coding: utf-8 -*-


{
    'name': "Additional Product Fields",
    'summary': """This module allow you to add custom fields on Products""",
    'description': """
		Custom Products fields .

    """,
    'author': "Rajeev Kumar.",
    'website': "",
    'images': [],
    'version': '1.0',
    'category' : 'sale',
    'depends': ['base','web','sale','purchase'],
    'data':[
        'views/products_view.xml',
		'views/sale_view.xml',
		'views/partner_view.xml',
		'Security/ir.model.access.csv',
    ],
    'installable' : True,
    'application' : False,
    'auto_install' : False,
}
