# -*- coding: utf-8 -*-
##############################################################################
import logging
from itertools import chain
from odoo.http import request
from odoo import models, fields, api

_logger = logging.getLogger(__name__)
USER_PRIVATE_FIELDS = ['password']
concat = chain.from_iterable


class LoginUserDetail(models.Model):
    _inherit = 'res.users'

    @api.model
    def check_credentials(self, password):
        result = super(LoginUserDetail, self).check_credentials(password)
        ip_address = request.httprequest.environ['REMOTE_ADDR']
        vals = {'name': self.name,
                'ip_address': ip_address
                }
        self.env['login.detail'].sudo().create(vals)
        return result

    # def write(self, vals):
    #     for user in self:
    #         log_out = fields.Datetime.now()
    #         print("log_out_time::::::::::::::::::::::")
    #         user_history = self.env['login.detail'].search([('user_id', '=', user.id)])
    #         print("kkkkkkk::::::::::::::::::;",user_history)
    #         user_history.write({'log_out_time': log_out_time})
    #     return super(LoginUserDetail, self).write(vals)


class LoginUpdate(models.Model):
    _name = 'login.detail'

    _order = 'date_time desc, id desc'


    name = fields.Char(string="User Name")
    date_time = fields.Datetime(string="Login Date And Time", default=lambda self: fields.datetime.now())
    ip_address = fields.Char(string="IP Address")
    log_out_time = fields.Datetime(string="Logout Date And Time")

