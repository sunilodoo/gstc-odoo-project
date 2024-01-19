# -*- coding: utf-8 -*-


{
    'name': "Custom Project/Task View",
    'summary': """ Customize Project/Task view by adding image field in new tab """,
    'description': """
Customize Project/Task view by adding image field in new tab
    """,
    'author': "Rajeev Kumar.",
    'website': "",
    'images': [],
    'version': '1.0',
    'category' : 'sale',
    'depends': ['base','sale', 'purchase','project'],
    'data':[
        'views/custom_task_view.xml',
        'views/custom_lead_view.xml',
		'Security/ir.model.access.csv',
    ],
    'installable' : True,
    'application' : False,
    'auto_install' : False,
}
