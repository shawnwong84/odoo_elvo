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

    def action_to_process(self):
        self.resi_status = 'to_process'

    def action_to_sent(self):
        self.resi_status = 'sent'

    def action_to_printed(self):
        self.resi_status = 'printed'

    def action_to_reprinted(self):
        self.resi_status = 'reprinted'