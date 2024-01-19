# -*- coding: utf-8 -*-
from odoo import models, fields, osv, api, _
from odoo.tools.translate import _
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.exceptions import Warning
from datetime import timedelta
import datetime

class ProjectTask(models.Model):
	_inherit = 'project.task'

	task_image = fields.One2many('task.image','img_id',string="Image")

class TaskImage(models.Model):
	_name = 'task.image'

	name = fields.Char('Name')
	image = fields.Binary('Image')
	img_id = fields.Many2one('project.task', string='Img ID')
