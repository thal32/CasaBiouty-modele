from odoo import models, fields

class LookBookTheme(models.Model):
    _name = 'look.book.theme'
    _description = 'Thème Look Book'

    name = fields.Char(string="Nom du Thème", required=True)
    description = fields.Text(string="Description")
    gallery_ids = fields.One2many('look.book.gallery', 'theme_id', string="Galeries")
    image = fields.Binary(string="Image de couverture", attachment=True)
    website_published = fields.Boolean(string="Publié sur le site web", default=True)