from odoo import models, fields, api, _


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    hide_create_payment = fields.Boolean(compute="_compute_hide_create_payment")
    difference_amount = fields.Float("Difference Amount Each Marketplace")

    @api.depends("amount")
    def _compute_hide_create_payment(self):
        for x in self:
            if x.amount >= 10000000:
                x.hide_create_payment = True
            else:
                x.hide_create_payment = False

    def confirm_payment_to_bod(self):
        self.action_create_payments()
        account_move = self.env['account.move'].search([('name', '=', self.communication)])
        account_move.payment_state = 'not_paid'

class PoValidationPayment(models.TransientModel):
    _name = 'po.validation.payment'
    _description = 'PO Validation Payment'

    communication = fields.Char()
    payment_difference_handling = fields.Selection([('open', 'Keep open'), ('reconcile', 'Mark invoice as fully paid')],
                                                   string="Payment Difference Handling")
    payment_difference = fields.Float("Payment Difference")