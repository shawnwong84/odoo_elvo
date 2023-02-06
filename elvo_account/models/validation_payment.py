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
        context = {}
        all_fields = self.fields_get()
        for field_name, field_value in all_fields.items():
            if field_value['type'] in ['char', 'text', 'integer', 'float', 'boolean', 'datetime']:
                context[f'default_{field_name}'] = getattr(self, field_name)
        print(all_fields)
        return {
            'name': _('Confirm Payment'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'po.validation.payment',
            'target': 'new',
            'context': context,
        }

class PoValidationPayment(models.TransientModel):
    _name = 'po.validation.payment'
    _description = 'PO Validation Payment'

    communication = fields.Char()
    payment_difference_handling = fields.Selection([('open', 'Keep open'), ('reconcile', 'Mark invoice as fully paid')],
                                                   string="Payment Difference Handling")
    payment_difference = fields.Float("Payment Difference")

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        context = self._context
        for field_name, field_value in context.items():
            if field_name.startswith('default_'):
                res[field_name[8:]] = field_value
        return res

    def button_cancel(self):
        return {
            'type': 'ir.actions.act_window_close'
        }

    def approve_button(self):
        account_move = self.env['account.move'].search([('name', '=', self.communication)])
        payment_state = 'partial' if self.payment_difference_handling == 'open' and self.payment_difference > 0 else 'not_paid'
        account_move.payment_state = payment_state
        payment_register = self.env['account.payment.register'].browse(self.ids)
        payment_register.action_create_payments()
        return {
            'type': 'ir.actions.act_window_close'
        }