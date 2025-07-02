{
    'name': 'HK Front',
    'description': 'Front du site web Odoo',
    'category': '',
    'version': '17.0.0.0.0',
    'author': 'matthieu',
    'license': 'LGPL-3',
    'depends': ['website', 'website_sale', 'website_sale_wishlist'],
    'data': [
        'views/home.xml',
        'views/layout.xml',
        'views/shop.xml',
        'views/fields_shop.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/hk_front/static/src/js/hk_js.js',
            '/hk_front/static/src/scss/hk_style.scss',
        ],
    },
}
