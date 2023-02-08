# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
	_inherit = 'sale.order'

	payment_history_ids = fields.One2many('advance.payment.history','order_id',string="Advanvce Payment Information")

	def set_sale_advance_payment(self):
		view_id = self.env.ref('akm_advance_payment.sale_advance_payment_wizard')
		if view_id:
			pay_wiz_data={
				'name' : _('Sale Advance Payment'),
				'type' : 'ir.actions.act_window',
				'view_type' : 'form',
				'view_mode' : 'form',
				'res_model' : 'sale.advance.payment',
				'view_id' : view_id.id,
				'target' : 'new',
				'context' : {
							'name':self.name,
							'order_id':self.id,
							'total_amount':self.amount_total,
							'company_id':self.company_id.id,
							'currency_id':self.currency_id.id,
							'date_order':self.date_order,
							'currency_rate':self.currency_rate,
							'partner_id':self.partner_id.id,
							 },
			}
		return pay_wiz_data
