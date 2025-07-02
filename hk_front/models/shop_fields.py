# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    rem_product_custom = fields.Float(
        string='Remise',
    )