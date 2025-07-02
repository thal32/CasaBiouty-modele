from odoo import models, fields

class LookBookGallery(models.Model):
    _name = 'look.book.gallery'
    _description = 'Galerie associée à un thème (ex : Trend Fashion)'

    name = fields.Char(string="Nom de la galerie", required=True)
    theme_id = fields.Many2one('look.book.theme', string="Thème associé", required=True)
    media_ids = fields.One2many('look.book.media', 'gallery_id', string="Médias de la galerie")
    description = fields.Text(string="Description de la galerie")
    image = fields.Binary(string="Image", attachment=True)