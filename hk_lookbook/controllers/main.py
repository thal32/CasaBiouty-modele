# from odoo import http
# from odoo.http import request

# class LookBookController(http.Controller):

#     @http.route(['/look-book'], type='http', auth='public', website=True)
#     def look_book_page(self, **kw):
#         books = request.env['look.book'].sudo().search([('is_published', '=', True)], order='id desc')
#         return request.render("hk_lookbook.website_look_books", {
#             'books': books,
#         })
