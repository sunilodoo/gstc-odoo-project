# -*- coding: utf-8 -*-
##############################################################################
{
    'name': 'Web Menu Hide/Show',
    'category': 'Web',
    'author': 'Rajeev Kumar',
	'website': '',
    'description': """
Web Menu Hide/Show
==================
    * Improves UI by allowing user to hide/show left menu bar
""",
    'version': '1.0',
    'depends': ['web'],
    'data' : [
        'views/web_menu_hide.xml'
    ],
    'qweb' : [
    ],
    'js' : [
        'static/src/js/web_menu_hide.js'
    ],
    'css' : [
        'static/src/css/web_menu_hide.css'
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
