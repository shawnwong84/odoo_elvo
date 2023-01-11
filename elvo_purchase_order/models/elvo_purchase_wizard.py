from odoo import models, fields, api


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
        self.purchase_order_id.picking_ids.action_cancel()
        return {
            'type': 'ir.actions.act_window_close'
        }
