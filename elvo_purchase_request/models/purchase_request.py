from odoo import models, fields, api, _


class PurchaseRequition(models.Model):
    _inherit = 'purchase.requisition'

    preparer = fields.Char("Preparer")
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('ongoing', 'Ongoing'),
        ('to_approve', 'To Approve'),
        ('in_progress', 'Confirmed'),
        ('open', 'Bid Selection'),
        ('done', 'Closed'),
        ('cancel', 'Cancelled')
    ])
    state_blanket_order = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('ongoing', 'Ongoing'),
        ('to_approve', 'To Approve'),
        ('in_progress', 'Confirmed'),
        ('open', 'Bid Selection'),
        ('done', 'Closed'),
        ('cancel', 'Cancelled')
    ])

    def to_approve(self):
        self.state = 'to_approve'

