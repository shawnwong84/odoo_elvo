from odoo import models, fields, api


class SupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'

    price_latest = fields.Float(string='Latest Price', compute='_compute_latest_price')

    @api.depends('product_tmpl_id')
    def _compute_latest_price(self):
        for line in self:
            get_data = line.env['purchase.order.line'].search(
                [('product_id', '=', line.product_id.id), ('state', 'in', ['done', 'purchase'])],
                order='write_date desc', limit=1)
            line.price_latest = get_data.price_unit