from odoo import models, fields


class ContactApproval(models.Model):
    _inherit = 'res.partner'

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('approve', 'Approve'),
            ('cancel', 'Cancel')
        ],
        default= 'draft',
        string='State'
    )

    approver_id = fields.Many2one('res.users', string='Approved By')

#========================== Function====================================
    def action_approve(self):
        for rec in self:
            rec.state = "approve"
            rec.approver_id= self.env.user

    def action_cancel(self):
        for rec in self:
            rec.state = "cancel"

    def action_reset(self):
        for rec in self:
            rec.state= "draft"
            rec.approver_id= None
