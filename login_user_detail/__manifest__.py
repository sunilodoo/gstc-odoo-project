# -*- coding: utf-8 -*-
##############################################################################
{
    'name': "User Log Details",
    'version': '10.0.3.0.0',
    'summary': """Login User Details & IP Address""",
    'description': """This module records login information of user""",
    'author': "Rajeev Kumar",
    'company': "",
    'maintainer': 'Rajeev Kumar',
    'website': "",
    'category': 'Tools',
    'depends': ['base'],
    'license': 'AGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'wizard/login_user_report_view.xml',
        'views/login_user_views.xml',
        'views/event_view.xml'],
    'images': [],
    'installable': True,
    'auto_install': False,
}
