# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class AccountPayment(models.Model):
	_inherit = "account.payment"

	check_advance_payment = fields.Boolean('Advance Payment', default=False)
	available_partner_bank_ids = fields.Many2one('res.partner.bank', string='Bank Account', readonly=False, store=True, domain="[('partner_id', '=', partner_id)]")

	@api.depends('journal_id', 'partner_id', 'partner_type', 'is_internal_transfer','check_advance_payment')
	def _compute_destination_account_id(self):
		res = super(AccountPayment, self)._compute_destination_account_id()
		for pay in self:
			if pay.is_internal_transfer:
				continue
			elif pay.partner_type == 'customer':
				if pay.check_advance_payment:
					if self.env.company.adv_account_id:
						self.destination_account_id = self.env.company.adv_account_id.id
			elif pay.partner_type == 'supplier':
				if pay.check_advance_payment:
					if self.env.company.adv_account_creditors_id:
						self.destination_account_id = self.env.company.adv_account_creditors_id.id
		return res


	def _seek_for_lines(self):
		liquidity_lines, counterpart_lines, writeoff_lines = super(AccountPayment, self)._seek_for_lines()
		counterpart_lines2 = self.env['account.move.line']
		if len(counterpart_lines)>1:
			for x in counterpart_lines:
				if x.account_id not in [self.env.company.adv_account_id, self.env.company.adv_account_creditors_id]:
					counterpart_lines2 += x
		else:
			counterpart_lines2 = counterpart_lines
	
		return liquidity_lines, counterpart_lines2, writeoff_lines


class AccountPaymentRegister(models.TransientModel):
	_inherit = "account.payment.register"

	customer_has_prepayment = fields.Monetary(compute='_compute_remain_prepayment', string="Advance Payment", store=True)
	advance_handling = fields.Selection([
		('no_apply', 'Not apply'),
		('apply', 'Apply'),
	], default='no_apply', )
	payment_difference_handling = fields.Selection(default='reconcile_multi_deduct')
	other_journal_id = fields.Many2one('account.account', string='Other Journal', domain="[('user_type_id', '=', 9), ('company_id', '=', company_id)]")

	@api.depends('partner_id','payment_type')
	def _compute_remain_prepayment(self):
		for reg in self:
			if reg.payment_type=='inbound':
				account = self.env.company.adv_account_id
			else:
				account = self.env.company.adv_account_creditors_id

			domain = [
				('account_id', '=', account.id),
				('move_id.state', '=', 'posted'),
				('partner_id', '=', reg.partner_id.id),
				('reconciled', '=', False)
			]

			totamount = 0
			for line in self.env['account.move.line'].search(domain):
				if line.currency_id == reg.currency_id:
					# Same foreign currency.
					amount = line.amount_residual_currency
				else:
					# Different foreign currencies.
					amount = reg.company_currency_id._convert(
						line.amount_residual,
						reg.currency_id,
						reg.company_id,
						line.date,
					)

				if reg.currency_id.is_zero(amount):
					continue
				totamount += amount

			reg.customer_has_prepayment = totamount

	@api.onchange('advance_handling')
	def action_apply_advance(self):
		if self.advance_handling=='apply':
			if self.payment_type=='inbound':
				account = self.env.company.adv_account_id
				label = 'Customer Advance'
			else:
				account = self.env.company.adv_account_creditors_id
				label = 'Vendor Advance'

			vals = {
				'payment_id': self.id,
				'account_id': account.id,
				'name': label,
				'amount': self.customer_has_prepayment,
				'is_prepayment': True
			}
			self.deduction_ids = [(0, 0, vals)]
		else:
			todel=[]
			for x in self.deduction_ids:
				if x.is_prepayment:
					todel.append((2, x.id))
			self.deduction_ids = todel

class AccountPaymentDeduction(models.TransientModel):
	_inherit = "account.payment.deduction"

	is_prepayment = fields.Boolean(string="Advance")