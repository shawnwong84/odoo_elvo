from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    def bod_validation_payment(self):
        self.payment_state = "in_payment"

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(AccountMove, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        last_run = self.env['ir.config_parameter'].sudo().get_param('elvo_account.last_run')
        now = fields.Datetime.now()
        today = fields.Date.today()
        account_move = self.env['account.move'].search(
                [('invoice_date_due', '<=', today), ('payment_state', 'in', ['not_paid', 'in_payment'])])
        for move in account_move:
            if now and last_run and float((now - fields.Datetime.from_string(last_run)).total_seconds() / 60) > 0.1:
                self.env['bus.bus'].sendone(
                    (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                    {'type': 'simple_notification', 'title': _('Payment Done'), 'message': _(
                        'Pembayaran atas Vendor ' + str(
                            move.partner_id.name) + ' dengan Kode ' + move.name + ' telah jatuh tempo pada hari ini, segera lakukan pembayaran.'),
                     'sticky': False, 'warning': False})
        self.env['ir.config_parameter'].sudo().set_param('elvo_account.last_run', fields.Datetime.now())
        return res
