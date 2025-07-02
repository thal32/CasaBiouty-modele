{
    "name": "Live Replay Website",
    "version": "1.0",
    "depends": ["website", "website_sale","product", "website_sale_wishlist",],
    "author": "Matthieu",
    "category": "Website",
    "data": [
        "security/ir.model.access.csv",
        "views/live_replay_views.xml",
        "views/replay_template.xml",       
    ],
    
    'assets': {
    'web.assets_frontend': [
        '/live_replay_website/static/src/scss/replay.scss',
        '/live_replay_website/static/src/js/replay.js',
    ],
},
    "installable": True,
}
