# -*- coding: utf-8 -*-


{
    'name': "Customized MIS Reporting For Purchase",
    'summary': """ Customized MIS Reporting For Purchase""",
    'description': """
This allow you to create/view MIS Reporting by Co-ordiantor For Purchase
    """,
    'author': "Rajeev Kumar.",
    'website': "",
    'images': [],
    'version': '1.0',
    'category' : 'custom',
    'depends': ['base','purchase', 'account','stock', 'delivery'],
    'data':[
        'views/po_mis_reporting_view.xml',
		'Security/ir.model.access.csv',
		'Security/record_rule.xml',
    ],
    'installable' : True,
    'application' : False,
    'auto_install' : False,
}
