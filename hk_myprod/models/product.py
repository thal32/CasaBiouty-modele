from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    sale_order_line_ids = fields.One2many(
        'sale.order.line',
        'product_id',
        string='Lignes de commande'
    )

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    total_sales = fields.Integer(
        string="Total Ventes",
        compute="_compute_total_sales",
        store=True
    )

    @api.depends('product_variant_ids.sale_order_line_ids.product_uom_qty')
    def _compute_total_sales(self):
        for template in self:
            total = 0
            for variant in template.product_variant_ids:
                lines = variant.sale_order_line_ids.filtered(
                    lambda l: l.order_id.state in ['sale', 'done']
                )
                total += sum(lines.mapped('product_uom_qty'))
            template.total_sales = total