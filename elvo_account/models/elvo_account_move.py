from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    def bod_validation_payment(self):
        self.payment_state = "in_payment"