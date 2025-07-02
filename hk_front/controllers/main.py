

from odoo import http
from odoo.http import request
import logging


_logger = logging.getLogger(__name__)

class LiveProductController(http.Controller):

    @http.route(['/live-products'], type='json', auth="public", website=True)
    def live_products(self, **kwargs):
        products = request.env['product.template'].sudo().search([
            ('is_live', '=', True),
            ('website_published', '=', True),
        ], limit=6)

        _logger.warning("Produits Live chargés : %s", products.mapped('name'))

        return request.env['ir.ui.view']._render_template(
            "website_sale.dynamic_filter_template_product_product_borderless_1",
            values={'records': products}
        )

