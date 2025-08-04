from odoo import http
from odoo.http import request

class HybridController(http.Controller):

    @http.route(['/hybride'], type='http', auth="public", website=True)
    def hybrid_product_list(self, **kwargs):
        # Récupérer les IDs d'attributs sélectionnés (peuvent être multiples)
        selected_ids = kwargs.getlist('attrib')  # par ex. ['5', '7']

        # Tous les attributs pour l'affichage des filtres
        all_attributes = request.env['product.attribute'].sudo().search([])

        # Filtrage des produits
        domain = []
        if selected_ids:
            variant_ids = request.env['product.template.attribute.value'].sudo().search([
                ('product_attribute_value_id', 'in', list(map(int, selected_ids)))
            ])
            product_ids = variant_ids.mapped('product_tmpl_id').ids
            domain = [('id', 'in', product_ids)]

        # Produits à afficher
        products = request.env['product.template'].sudo().search(domain)

        return request.render('hk_myprod.custom_search_result', {
            'products': products,
            'all_attributes': all_attributes,
            'selected_ids': list(map(int, selected_ids)),
        })


class CustomShopController(http.Controller):

    @http.route(['/shop'], type='http', auth='public', website=True)
    def custom_shop(self, **kwargs):
        products = request.env['product.template'].search([('sale_ok', '=', True)], limit=20)
        categories = request.env['product.public.category'].search([])
        attributes = request.env['product.attribute'].search([])

        pl_id = request.session.get('website_sale_current_pl', False)
        pricelist = request.env['product.pricelist'].browse(pl_id) if pl_id else request.env['product.pricelist'].search([], limit=1)

        website_sale_pricelists = request.env['product.pricelist'].search([])
        has_pricelist_dropdown = len(website_sale_pricelists) > 1

        return request.render('hk_myprod.products_custom_beta', {
            'products': products,
            'categories': categories,
            'attributes': attributes,
            'website': request.website,
            'pricelist': pricelist,
            'website_sale_pricelists': website_sale_pricelists,
            'hasPricelistDropdown': has_pricelist_dropdown,
        })


