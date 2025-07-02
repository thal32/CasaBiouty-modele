# from odoo import http
# from odoo.http import request

# class LiveReplayWebsite(http.Controller):

#     @http.route(['/replay/<slug:live_replay>'], type='http', auth='public', website=True)
#     def replay_detail(self, live_replay, **kw):
#         return request.render(
#             'live_replay_website.replay_detail_template',
#             {'replay': live_replay}
#         )