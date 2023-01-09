from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('to_approve_manager', 'To Approve Manager Finance'),
        ('to_approve_finance', 'To Approve Finance'),
        ('to_approve_bod', 'To Approve BOD'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)
    po_notes = fields.Selection([
        ('note1', 'MOHON KONFIRMASI SETELAH MENERIMA PO.'),
        ('note2', 'MOHON MENCANTUMKAN NOMOR PO PADA SURAT JALAN.'),
        ('note3', 'ALAMAT KIRIM BARANG SESUAI ALAMAT PENGIRIMAN DI PO.'),
        ('note4', 'FRANCO GUDANG ALAMAT PENGIRIMAN.')
    ], string="Notes")
    reason = fields.Char(string="Reason")

    def to_approve_manager(self):
        self.state = 'to_approve_manager'

    def to_approve_finance(self):
        self.state = 'to_approve_finance'

    def to_approve_bod(self):
        self.state = 'to_approve_bod'

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

class CancelPoWizard(models.TransientModel):
    _name = 'cancel.po.wizard'

    purchase_order_id = fields.Many2one('purchase.order', string="Purchase Order", readonly=True)
    reason = fields.Char(string="Reason")

    def button_cancel(self):
        return {
            'type': 'ir.actions.act_window_close'
        }

    def approve_button(self):
        return {
            'name': 'Cancel PO',
            'type': 'ir.actions.act_window',
            'res_model': 'confirmation.to.cancel',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_purchase_order_id': self.purchase_order_id.id,
                'default_reason': self.reason,
            }
        }


class ConfirmationToCancel(models.TransientModel):
    _name = 'confirmation.to.cancel'

    purchase_order_id = fields.Many2one('purchase.order', string="Purchase Order")
    reason = fields.Char(string="Reason")

    def button_cancel(self):
        return {
            'type': 'ir.actions.act_window_close'
        }

    def approve_button(self):
        self.purchase_order_id.state = 'cancel'
        self.purchase_order_id.reason = self.reason
        return {
            'type': 'ir.actions.act_window_close'
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