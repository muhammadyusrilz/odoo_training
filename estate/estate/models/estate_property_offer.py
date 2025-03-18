from email.policy import default

from dateutil.relativedelta import relativedelta

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class EstateOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer Made"
    _rec_name = "property_id"

    price = fields.Float()
    status = fields.Selection(
        [
            ("accepted","Accepted"),
            ("refused","Refused")
        ], copy = False,
    )
    validity = fields.Integer(String = "Validity",default = 7)
    date_deadline = fields.Date(String = "DeadLine", compute= "_compute_date_deadline", inverse = "_inverse_date_deadline")

    partner_id = fields.Many2one("res.partner",required=True, string="Partner")
    property_id = fields.Many2one("estate.property",required=True, string="Property")
    property_type_id = fields.Many2one(related = "property_id.property_type_id")

#============================== Compute Methods ===========================================

    @api.depends("validity")
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = fields.Date.today() + relativedelta(days= offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - fields.Date.today()).days

    def action_accept(self):
        self.ensure_one()
        if self.status == "accepted":
            raise UserError(_("Sold"))
        self.status= "accepted"
        self.property_id.selling_price= self.price
        self.property_id.state= 'sold'

    def action_refuse(self):
        self.ensure_one()
        if self.status == "refused":
            raise UserError(_("refused"))
        self.status = "refused"
        self.property_id.selling_price = 0