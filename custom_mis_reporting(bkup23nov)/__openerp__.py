# -*- coding: utf-8 -*-


{
    'name': "Customized MIS Reporting",
    'summary': """ Customized MIS Reporting """,
    'description': """
This allow you to create/view MIS Reporting by Co-ordiantor
    """,
    'author': "Rajeev Kumar.",
    'website': "",
    'images': [],
    'version': '1.0',
    'category' : 'custom',
    'depends': ['base','sale',],
    'data':[
        'views/mis_reporting_view.xml',
		'Security/ir.model.access.csv',
    ],
    'installable' : True,
    'application' : False,
    'auto_install' : False,
}
