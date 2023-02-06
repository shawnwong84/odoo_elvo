from odoo import models, fields, api

class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    type_of_payment = fields.Selection([
        ('regular', 'Regular Payment'),
        ('down_payment', 'Down Payment'),
    ], string="Create Payment", default='regular')
    dp_amount = fields.Monetary(string="Down Payment Amount")

    @api.onchange('dp_amount')
    def onchange_dp_amount(self):
        if self.type_of_payment == 'down_payment':
            self.amount = self.dp_amount

    @api.onchange('type_of_payment')
    def onchange_type_of_amount(self):
        if self.type_of_payment == 'down_payment':
            self.dp_amount = self.amount

class AccountMove(models.Model):
    _inherit = 'account.move'

    payment_state = fields.Selection(selection_add=[('down_payment', 'Down Payment')])