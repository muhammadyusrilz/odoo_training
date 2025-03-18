from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_rental_order = fields.Boolean()
    rental_start_date = fields.Datetime()
    rental_return_date = fields.Datetime()
    duration_days = fields.Integer(compute='_compute_duration_days')
    status_rental = fields.Selection(
        [
            ('draft', 'Draft'),
            ('reserved', 'Reserved'),
            ('returned', 'Returned'),
            ('cancelled', 'Cancelled')
        ],
        string = 'Status Rental',
        default = 'draft'
    )

    # ============ Function ================

    @api.depends('rental_start_date', 'rental_return_date')
    def _compute_duration_days(self):
        for rec in self:
            if rec.rental_start_date and rec.rental_return_date:
                start_date = rec.rental_start_date.replace(hour=0, minute=0, second=0)
                return_date = rec.rental_return_date.replace(hour=0, minute=0, second=0)
                rec.duration_days = (return_date - start_date).days
            else:
                rec.duration_days=0

    def action_confirm(self):
        result= super(SaleOrder,self).action_confirm()
        today = fields.Datetime.now()
        for rec in self:
            if rec.rental_start_date and rec.rental_return_date:
                if rec.rental_start_date <= today < rec.rental_return_date:
                    rec.status_rental = "reserved"
        return result

    def action_rental_confirm(self):
        today = fields.Datetime.now()
        for rec in self:
            if rec.rental_start_date and rec.rental_return_date:
                if rec.rental_start_date <= today <= rec.rental_return_date:
                    rec.status_rental = 'reserved'

    def action_rental_reserved(self):
        for rec in self:
            rec.status_rental = 'reserved'

    def action_rental_returned(self):
        for rec in self:
            rec.status_rental = 'returned'