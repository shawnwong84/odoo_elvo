from odoo import models, fields, api, _

class AccountMoveReversal(models.TransientModel):
    _inherit = "account.move.reversal"

    create_refund = fields.Selection([
        ('percentage', 'Refund (Percentage)'),
        ('fixed', 'Refund (Fixed Amount)'),
    ], default='fixed')
    refund_percentage = fields.Float(string='Refund Amount')
    refund_fixed = fields.Float(string='Refund Amount')