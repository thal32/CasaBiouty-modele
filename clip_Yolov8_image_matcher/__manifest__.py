
{
    "name": 'CLIP + YOLOv8 Image Comparator',
    "version": "1.0",
    "author": "Matthieu",
    "summary": "Compare two images using OpenAI's CLIP and YoloV8",
    "category": "IA",
    "depends": ["base","product",],
    "data": [
        "security/ir.model.access.csv",
        "views/view.xml",
        "views/menus.xml",
        "views/view_product.xml",
    ],
    'external_dependencies': {
        'python': [
            'torch',
            'clip',            
            'Pillow',
            'numpy',
            'ultralytics',
        ],
    },
    "assets": {},
    "installable": True,
    "application": True,
}
