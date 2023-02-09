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
        ('receipt', 'Receipt'),
        ('under', 'Under Receipt'),
    ])
    is_over_receipt = fields.Boolean(compute='compute_receipt_status', store=True)

    @api.depends('order_line.move_ids.quantity_done', 'order_line.product_qty')
    def compute_receipt_status(self):
        for x in self:
            for line in x.order_line:
                if line.move_ids:
                    qty_done = sum(line.move_ids.mapped('quantity_done'))
                    uom = line.product_qty
                    max = uom + uom * x.tolerance
                    if qty_done > max:
                        x.receipt_status = 'over'
                    elif qty_done >= line.product_qty and qty_done < max:
                        x.receipt_status = 'receipt'
                    elif qty_done < line.product_qty or qty_done == 0:
                        x.receipt_status = 'under'
                    else:
                        x.receipt_status = 'under'
            x.is_over_receipt = True if x.receipt_status == 'over' else False


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

    # receipt_status = fields.Selection([
    #     ('over', 'Over Receipt'),
    #     ('receipt', 'Receipt'),
    #     ('under', 'Under Receipt'),
    # ], string="Receipt Status", compute="_compute_receipt_status")
    is_over_receipt = fields.Boolean()

    # @api.depends('name', 'move_ids_without_package.quantity_done', 'move_ids_without_package.product_uom_qty')
    # def _compute_receipt_status(self):
    #     tolerance = self.purchase_id.tolerance
    #     for line in self.move_lines:
    #         if self.receipt_status:
    #             break
    #         uom = line.product_uom_qty
    #         qty_done = line.quantity_done
    #         max = uom + uom * tolerance
    #         if qty_done > max:
    #             self.receipt_status = 'over'
    #         elif qty_done >= line.product_uom_qty and qty_done < max:
    #             self.receipt_status = 'receipt'
    #         elif qty_done < line.product_uom_qty or qty_done == 0:
    #             self.receipt_status = 'under'
    #         else:
    #             self.receipt_status = 'under'
    #     self.receipt_status and self.purchase_id.write({'receipt_status': self.receipt_status})



