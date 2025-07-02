
from odoo import http
from odoo.http import request
import torch
import clip
from PIL import Image
import io
import base64
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class ClipImageMatcherController(http.Controller):

    @http.route('/clip_match/upload', type='http', auth='user', website=True, csrf=False)
    def upload_image(self, **kwargs):
        return request.render("clip_image_matcher.upload_form", {})

    @http.route('/clip_match/result', type='http', auth='user', methods=['POST'], csrf=False)
    def match_image(self, **kwargs):
        upload_file = kwargs.get('image_file')
        image_data = upload_file.read()
        image = Image.open(io.BytesIO(image_data))

        model, preprocess = clip.load("ViT-B/32")
        image_tensor = preprocess(image).unsqueeze(0)
        with torch.no_grad():
            vector = model.encode_image(image_tensor).cpu().numpy()

        records = request.env['clip.image.matcher'].sudo().search([])
        similarities = []

        for r in records:
            if r.image_1:
                vec = request.env['clip.image.matcher'].create_clip_vector(r.image_1)
                score = cosine_similarity(vector, vec.reshape(1, -1))
                similarities.append((r, float(score)))

        similarities.sort(key=lambda x: -x[1])
        top_matches = similarities[:5]

        return request.render("clip_image_matcher.match_result", {
            'matches': [(rec.name, rec.image_1, sim) for rec, sim in top_matches]
        })
