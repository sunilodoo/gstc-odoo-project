
from odoo import models, fields, api
from datetime import datetime
from dateutil import relativedelta
import time
from odoo import _
from odoo.exceptions import UserError



class EventEvent(models.Model):
    """Model for managing Event"""
    _name = 'event.event.custom'

    name = fields.Char('Name', required=True, copy=False)
    
    
    start_date = fields.Datetime(string="Start date",
                                 default=lambda self: fields.datetime.now(),
                                 )
    end_date = fields.Datetime(string="End date")

    location = fields.Text('Location')

    seats = fields.Integer('Seats')
  
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'),
                              ('done', 'Done'),
                              ],
                             string="State", default="draft")

    # _sql_constraints = [
    #         ('check','CHECK((start_date <= end_date))',"End date must be greater then start date")  
    # ]



    @api.multi
    def create_end_date(self, values):
        """Crete method for sequencing and checking dates while creating"""
        # start_date = values['start_date']
        # end_date = values['end_date']
        if self.start_date <= self.end_date:
            raise UserError(_('End date must be greater then start date'))





    def action_event_confirm(self):
        """Button action to confirm"""
        self.state = "confirm"
 


