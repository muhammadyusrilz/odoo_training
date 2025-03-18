from odoo import models, fields, api

class ProductTemplate(models.Model):
   _inherit = 'product.template'

   is_rent = fields.Boolean(string='Can Be Rented')
   count_rent = fields.Integer(compute="_compute_count_rent")

# =============== Function =============
   @api.depends('is_rent')
   def _compute_count_rent(self):
        # rent_count = self.env['product.template'].search_count([('is_rent','=','True')])
        for rent in self:
            rent.count_rent = self.env['sale.order.line'].search_count([
                ('product_template_id', '=', rent.id),
                ('order_id.status_rental', '=', 'reserved')
            ])

   def action_view_reserved_orders(self):
       sale_orders = self.env['sale.order.line'].search([
           ('product_id.product_tmpl_id', '=', self.id),
           ('order_id.status_rental', '=', 'reserved')
       ]).mapped('order_id')
       return {
           'name': 'Reserved Sale Orders',
           'type': 'ir.actions.act_window',
           'view_mode': 'tree,form',
           'res_model': 'sale.order',
           'domain': [('id', 'in', sale_orders.ids)],
           'views': [(self.env.ref('rental_sales.view_sale_order_reserved_tree').id, 'tree'),
                     (False, 'form')],
           'context': {'default_status_rental': 'reserved'},
       }