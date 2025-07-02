{
    "name": "HK Look Book",
    "version": "1.0",
    "summary": "Look Book personnalisé pour site web Odoo",
    "category": "Website",
    'author': 'matthieu',
    "depends": ["base","website", 'product',],
    "data": [
        'security/ir.model.access.csv',
        "views/lookbook_template.xml",
        'views/look_book_views.xml',
        'views/look_book_gallery_views.xml',
        'views/lookbook_media_product_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/hk_lookbook/static/src/scss/lookbook.scss',
            '/hk_lookbook/static/src/js/lookbook.js',
        ],
    },
    "application": True,
    "installable": True
}
