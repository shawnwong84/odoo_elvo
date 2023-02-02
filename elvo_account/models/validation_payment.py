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
        return {
            'name': _('Confirm Payment'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'po.validation.payment',
            'target': 'new',
            'context': {
                'default_communication': self.communication,
                'default_payment_difference_handling': self.payment_difference_handling,
                'default_payment_difference': self.payment_difference,
            }
        }


class PoValidationPayment(models.TransientModel):
    _name = 'po.validation.payment'
    _description = 'PO Validation Payment'

    communication = fields.Char()
    payment_difference_handling = fields.Selection([('open', 'Keep open'), ('reconcile', 'Mark invoice as fully paid')],
                                                   string="Payment Difference Handling")
    payment_difference = fields.Float("Payment Difference")

    def button_cancel(self):
        return {
            'type': 'ir.actions.act_window_close'
        }

    def approve_button(self):
        if self.payment_difference_handling == "open":
            self.env['account.payment'].browse(self._context.get('active_id')).post()
        elif self.payment_difference_handling == "reconcile":
            self.env['account.payment'].browse(self._context.get('active_id')).reconcile()
            account_move_id = self.env['account.move'].search([('name', '=', self.communication)])
            account_move_id.payment_state = 'not_paid'
            return {
                'type': 'ir.actions.act_window_close'
            }
