from odoo import models, fields


class LookBookMedia(models.Model):
    _name = 'look.book.media'
    _description = 'Média/image dans une galerie'

    name = fields.Char(string="Titre de la photo", required=True)
    gallery_id = fields.Many2one('look.book.gallery', string="Galerie", required=True)
    image = fields.Binary(string="Image", required=True)
    product_ids = fields.One2many('look.book.media.product', 'media_id', string="Produits portés")
    description = fields.Text(string="Description de la photo")