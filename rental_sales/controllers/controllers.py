# -*- coding: utf-8 -*-
# from odoo import http


# class RentalSales(http.Controller):
#     @http.route('/rental_sales/rental_sales', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rental_sales/rental_sales/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rental_sales.listing', {
#             'root': '/rental_sales/rental_sales',
#             'objects': http.request.env['rental_sales.rental_sales'].search([]),
#         })

#     @http.route('/rental_sales/rental_sales/objects/<model("rental_sales.rental_sales"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rental_sales.object', {
#             'object': obj
#         })

