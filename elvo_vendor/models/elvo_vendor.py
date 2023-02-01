from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    taxes_id = fields.Many2one('account.tax', string='Taxes')