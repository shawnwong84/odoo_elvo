# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    available_partner_bank_ids = fields.Many2many(
        comodel_name='res.partner.bank',
        compute='_compute_available_partner_bank_ids',
    )
    payment_difference_handling = fields.Selection(
        selection_add=[
            ("reconcile_multi_deduct", "With Multi Deduction")
        ],
        ondelete={"reconcile_multi_deduct": "cascade"},
    )
    currency_company = fields.Many2one('res.currency', string='Curr Company', store=True, readonly=False,
        compute='_compute_currency_company',)
    amount_company = fields.Monetary(currency_field='currency_company', )
    deduct_residual = fields.Monetary(
        string="Remainings", compute="_compute_deduct_residual"
    )
    deduction_ids = fields.One2many(
        comodel_name="account.payment.deduction",
        inverse_name="payment_id",
        string="Deductions",
        copy=False,
        help="Sum of deduction amount(s) must equal to the payment difference",
    )

    @api.depends('partner_id', 'company_id', 'payment_type')
    def _compute_available_partner_bank_ids(self):
        for pay in self:
            if pay.payment_type == 'inbound':
                pay.available_partner_bank_ids = pay.journal_id.bank_account_id
            else:
                pay.available_partner_bank_ids = pay.partner_id.bank_ids\
                        .filtered(lambda x: x.company_id.id in (False, pay.company_id.id))._origin

    @api.depends('amount')
    def _compute_payment_difference(self):
        for wizard in self:
            if wizard.source_currency_id == wizard.currency_id:
                # Same currency.
                if wizard.amount_company:
                    amount_payment_currency = wizard.company_id.currency_id._convert(wizard.amount_company, wizard.currency_id, wizard.company_id, wizard.payment_date, round=False)
                    wizard.payment_difference = wizard.source_amount_currency - amount_payment_currency
                else:
                    wizard.payment_difference = wizard.source_amount_currency - wizard.amount
            elif wizard.currency_id == wizard.company_id.currency_id:
                # Payment expressed on the company's currency.
                wizard.payment_difference = wizard.source_amount - wizard.amount
            else:
                # Foreign currency on payment different than the one set on the journal entries.
                amount_payment_currency = wizard.company_id.currency_id._convert(wizard.source_amount, wizard.currency_id, wizard.company_id, wizard.payment_date)
                wizard.payment_difference = amount_payment_currency - wizard.amount

    @api.onchange('amount_company')
    def _onchange_amount_company(self):
        for x in self:
            amount = x.company_id.currency_id._convert(x.amount_company, x.currency_id, x.company_id, x.payment_date, round=False)
            x.amount = amount

    @api.depends('company_id')
    def _compute_currency_company(self):
        for wizard in self:
            wizard.currency_company = wizard.company_id.currency_id

    def action_create_payments(self):
        if self.payment_difference_handling == "reconcile_multi_deduct":
            self = self.with_context(
                skip_account_move_synchronization=True,
                dont_redirect_to_payments=True,
            )
        return super().action_create_payments()

    @api.constrains("deduction_ids", "payment_difference_handling")
    def _check_deduction_amount(self):
        prec_digits = self.env.user.company_id.currency_id.decimal_places
        # for rec in self:
        #     if rec.payment_difference_handling == "reconcile_multi_deduct":
        #         if float_compare(rec.payment_difference, sum(rec.deduction_ids.mapped("amount")),
        #                           precision_digits=prec_digits,) != 0:
        #             raise UserError(_("The total deduction should be %s") % rec.payment_difference)

    @api.depends("payment_difference", "deduction_ids")
    def _compute_deduct_residual(self):
        for rec in self:
            rec.deduct_residual = rec.payment_difference - sum(
                rec.deduction_ids.mapped("amount")
            )

    def _create_payment_vals_from_wizard(self):
        payment_vals = super()._create_payment_vals_from_wizard()
        if (
            self.payment_difference
            and self.payment_difference_handling == "reconcile_multi_deduct"
        ):
            payment_vals["write_off_line_vals"] = [
                self._prepare_deduct_move_line(deduct)
                for deduct in self.deduction_ids.filtered(lambda l: not l.open)
            ]
        return payment_vals

    def _prepare_deduct_move_line(self, deduct):
        return {
            "name": deduct.name,
            "amount": deduct.amount,
            "account_id": deduct.account_id.id,
        }
