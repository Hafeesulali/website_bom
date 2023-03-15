from odoo import models, fields, api
from ast import literal_eval


class BomProducts(models.TransientModel):
    _inherit = "res.config.settings"

    product_ids = fields.Many2many("product.template", string="products")

    def set_values(self):
        res = super(BomProducts, self).set_values()
        self.env['ir.config_parameter'].sudo().\
            set_param('website_bom.product_ids', self.product_ids.ids)
        return res

    @api.model
    def get_values(self):
        res = super(BomProducts, self).get_values()
        with_user = self.env['ir.config_parameter'].sudo()
        com_products = with_user.get_param('website_bom.product_ids')
        res.update(product_ids=[(6, 0, literal_eval(com_products))] if com_products else False, )
        return res
