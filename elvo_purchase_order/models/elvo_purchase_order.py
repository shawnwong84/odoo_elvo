from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('to_approve_manager', 'To Approve Manager Finance'),
        ('to_approve_bod', 'To Approve BOD'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)
    invoice_status = fields.Selection(selection_add=[('over', 'Over Receipt')])
    po_note = fields.Many2one('purchase.order.note', string="Notes")
    tolerance = fields.Float(string="Tolerance", default=0.15)
    reason = fields.Char(string="Reason")
    receipt_status = fields.Selection([
        ('over', 'Over Receipt'),
        ('under', 'Under Receipt'),
    ])

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        if self.amount_total < 1000000:
            self.state = 'purchase'
        elif self.amount_total >= 1000000:
            self.state = 'to_approve_manager'
            self.env['stock.picking'].search([('purchase_id', '=', self.id)]).write({'state': 'waiting'})
        return res

    def to_approve_manager(self):
        if self.amount_total < 10000000:
            self.state = 'purchase'
            self.env['stock.picking'].search([('purchase_id', '=', self.id)]).write({'state': 'assigned'})
        elif self.amount_total >= 10000000:
            self.state = 'to_approve_bod'

    def to_approve_bod(self):
        self.state = 'purchase'
        self.env['stock.picking'].search([('purchase_id', '=', self.id)]).write({'state': 'assigned'})

    def cancel_po_wizard(self):
        return {
            'name': 'Cancel PO',
            'type': 'ir.actions.act_window',
            'res_model': 'cancel.po.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_purchase_order_id': self.id,
            }
        }


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    price_latest = fields.Float(string='Latest Price', compute='_compute_latest_price')

    @api.depends('product_id')
    def _compute_latest_price(self):
        for line in self:
            get_data = line.env['purchase.order.line'].search(
                [('product_id', '=', line.product_id.id), ('state', 'in', ['done', 'purchase'])],
                order='write_date desc', limit=1)
            line.price_latest = get_data.price_unit
            self.env['product.supplierinfo'].search([('product_tmpl_id', '=', line.product_id.product_tmpl_id.id),
                                                        ('name', '=', line.order_id.partner_id.id)]).write(
                {'price_latest': get_data.price_unit})


class Picking(models.Model):
    _inherit = 'stock.picking'

    is_over_receipt = fields.Boolean(string="Over Receipt", compute='_compute_over_receipt')

    @api.depends('name', 'move_ids_without_package.quantity_done', 'move_ids_without_package.product_uom_qty')
    def _compute_over_receipt(self):
        tolerance = self.purchase_id.tolerance
        is_over = False
        for line in self.move_lines:
            if is_over:
                break
            uom = line.product_uom_qty
            qty_done = line.quantity_done
            max = uom + uom * tolerance
            is_over = True if qty_done > max else False
        self.is_over_receipt = is_over
        is_over and self.purchase_id.write({'receipt_status': 'over'})
