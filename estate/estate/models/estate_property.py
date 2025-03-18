from dataclasses import fields
from datetime import date

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "model estate property"

    active = fields.Boolean(default=True, invisible=True)
    name = fields.Char(string="Title", required=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("received", "Offer Received"),
            ("accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancel", "Cancel")
        ],
        required=True,
        copy=False,
        default="new"
    )

    description = fields.Text()

    def _default_date(self):
        return fields.Date.today()

    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(default=_default_date, string="Date Availability")
    expected_price = fields.Float(required=True, string="Expected Price")
    selling_price = fields.Float(string="Selling Price", compute= "_best_price")
    bedrooms = fields.Integer()
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = (
        fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]))
    total_area = fields.Integer(compute= "_compute_total", inverse = "_inverse_total")


    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    sales_person_id = fields.Many2one("res.users", string="Sales Person")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    tag_ids = fields.Many2many("estate.property.tag")

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for rec in self:
            rec.total_area= rec.living_area+rec.garden_area

    def _inverse_total(self):
        for rec in self:
            rec.living_area = rec.total_area-rec.garden_area

    @api.onchange("garden")
    def _compute_garden_area(self):
        if not self.garden:
            self.garden_area = 0

    @api.onchange("date_availability")
    def _compute_date_availability(self):
        if self.date_availability  < date.today():
            return {"warning" : {"title":_("Warning"), "message" : _("Date")}}

    def action_sold(self):
        for rec in self:
            if rec.state == "sold":
                raise UserError(_("Propery set as sold, can't be cancelled"))
            rec.state = "sold"

    def action_cancel(self):
        for rec in self:
            if rec.state == "cancel":
                raise UserError(_("Property set as cancel, can't be sold"))
            rec.state = "cancel"

    def _best_price(self):
        for rec in self:
            selling_price = max(rec.offer_ids.mapped('price'))
            rec.selling_price = selling_price



