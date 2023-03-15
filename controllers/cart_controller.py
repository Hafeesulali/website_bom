from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import http
from odoo.http import request


class CartBom(WebsiteSale):
    @http.route()
    def cart(self, access_token=None, revive='', **post):
        res = super(CartBom, self).\
            cart(access_token=access_token, revive=revive, **post)
        order = request.website.sale_get_order()
        lst = request.env['ir.config_parameter'].\
            sudo().get_param('website_bom.product_ids')
        dict = {}
        product_list = [j.product_template_id.id for j in order.order_line]
        for product_id in product_list:
            if str(product_id) in lst:
                bom_list = [rec.product_id.name for rec in
                            request.env['mrp.bom.line'].
                            search([('parent_product_tmpl_id', '=', product_id)])]
                dict.update({
                    product_id: bom_list
                })
        print(dict)
        res.qcontext.update({
            'website_product_ids': dict
        })

        return res
