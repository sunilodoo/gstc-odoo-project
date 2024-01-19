# Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
# Copyright (C) Thinkopen Solutions <http://www.tkobr.com>.
# Copyright (C) Open Source Integrators <http://www.opensourceintegrators.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Web Sessions Management',
    'summary': '''Sessions timeout and forced termination.
        Multisession control. Login by calendar (week day hours).
        Remote IP filter and location.''',
    'author': 'Sunil Singh',
    'category': 'Extra Tools',
    'license': 'AGPL-3',
    'website': 'www.gstc.com',
    'version': '1.0',
    'depends': [
        
    ],
    'external_dependencies': {
        'python': ['num2words'],
    },
    # 'images': ['static/description/sessions_groups.png',
    #            'static/description/sessions_management.png',
    #            'static/description/sessions_pivot.png',
    #            'static/description/sessions_user_preferences.png',
    #            'static/description/sessions_users.png',],
    'data': [
        'security/ir.model.access.csv',
        'data/scheduler.xml',
        'views/res_users_view.xml',
        'views/res_groups_view.xml',
        'views/ir_sessions_view.xml',
        'views/webclient_templates.xml',
    ],
    'installable': True,
}
