from odoo import models, fields, api, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    retur_status = fields.Selection([
        ('retur', 'Retur'),
        ('refund', 'Refund'),
    ])
    resi_kirim = fields.Char(string='Resi Kirim')
    resi_retur = fields.Char(string='Resi Retur')
    resi_status = fields.Selection([
        ('to_process', 'To Process'),
        ('sent', 'Sent'),
        ('printed', 'Printed'),
        ('reprinted', 'Reprinted'),
    ], string="Status Resi")