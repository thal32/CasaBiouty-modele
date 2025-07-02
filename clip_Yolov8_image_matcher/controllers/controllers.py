from odoo import http

class ClipImageMatcherController(http.Controller):

    @http.route('/clip_match/upload', type='http', auth='user', website=True, csrf=False)
    def upload_image(self, **kwargs):
        return "Upload form placeholder"
