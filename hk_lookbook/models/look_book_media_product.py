

from odoo import models, fields

class LookBookMediaProduct(models.Model):
    _name = 'look.book.media.product'
    _description = 'Produit associé à une photo dans une galerie'

    media_id = fields.Many2one('look.book.media', string="Image Look Book", required=True, ondelete='cascade')
    product_id = fields.Many2one('product.template', string="Produit de la base", required=True)
    label = fields.Char(string="Nom personnalisé du produit")
    description = fields.Text(string="Description personnalisée (facultatif)")
