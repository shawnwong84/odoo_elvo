from odoo import models, fields, api, _


class PurchaseRequition(models.Model):
    _inherit = 'purchase.requisition'

    preparer = fields.Many2one('res.users', string='Preparer')
    hide_approve_button = fields.Boolean(compute='_compute_hide_approve_button')
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

    def _compute_hide_approve_button(self):
        if self.env.user == self.user_id:
            self.hide_approve_button = True
        else:
            self.hide_approve_button = False


    def to_approve(self):
        self.state = 'to_approve'

