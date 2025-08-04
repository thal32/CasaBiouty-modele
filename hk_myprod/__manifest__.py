{
    'name': 'hk my prod',
    'description': 'Produits de la boutique',
    'category': '',
    'version': '17.0.0.0.0',
    'author': 'matthieu',
    'license': 'LGPL-3',
    'depends': ['website', 'website_sale', 'website_sale_wishlist','product'],
    'data': [
        'views/shop.xml',
        'views/layout.xml',
        'views/acceuil.xml',
        'views/search.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/hk_myprod/static/src/scss/style.scss',
        ],
    },
}
