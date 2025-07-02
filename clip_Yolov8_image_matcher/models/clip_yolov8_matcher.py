from odoo import models, fields, api
from odoo.exceptions import ValidationError
import torch
import clip
from PIL import Image
import io
import base64
import numpy as np
import logging
from ultralytics import YOLO
import os
import pickle

_logger = logging.getLogger(__name__)

CLOTHING_CLASSES = [
    'short_sleeved_shirt', 'long_sleeved_shirt', 'short_sleeved_outwear', 'long_sleeved_outwear',
    'vest', 'sling', 'shorts', 'trousers', 'skirt',
    'short_sleeved_dress', 'long_sleeved_dress', 'vest_dress', 'sling_dress'
]

class MatchedProductLine(models.Model):
    _name = 'matched.product.line'
    _description = 'Produit similaire avec score'

    matcher_id = fields.Many2one('image.yolov8.image.matcher', string="Comparaison", required=True, ondelete='cascade')
    product_id = fields.Many2one('product.template', string="Produit", required=True)
    clip_similarity_score = fields.Float(string="Similarité (%)")

    product_name = fields.Char(string="Nom produit", related='product_id.name', store=True, readonly=True)
    product_image = fields.Image(string="Image produit", related='product_id.image_1920', store=False, readonly=True)


class ImageClothingMatcher(models.Model):
    _name = 'image.yolov8.image.matcher'
    _description = 'Clothing Comparison with AI'

    name = fields.Char("Nom")
    image_1 = fields.Image("Image 1", required=True)
    similarity_score = fields.Float("Score de similarité", readonly=True)
    similarity_display = fields.Html(string="Score (%)", compute="_compute_similarity_display", sanitize=False)

    matched_product_line_ids = fields.One2many('matched.product.line', 'matcher_id', string="Produits similaires")

    @api.model
    def _get_models(self):
        if not hasattr(self.env, "_clip_model"):
            self.env._clip_model, self.env._clip_preprocess = clip.load("ViT-B/32", device="cpu")
            self.env._clip_model.eval()

        if not hasattr(self.env, "_yolo_model"):
            module_path = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(module_path, "deepfashion2_yolov8s-seg.pt")
            if not os.path.exists(model_path):
                raise ValidationError(f"Fichier modèle YOLO introuvable : {model_path}")
            _logger.info(f"Chargement du modèle YOLO depuis : {model_path}")
            self.env._yolo_model = YOLO(model_path)

        return self.env._clip_model, self.env._clip_preprocess, self.env._yolo_model

    def _extract_clothing_tensors(self, image_binary):
        _, preprocess, yolo_model = self._get_models()
        image_data = base64.b64decode(image_binary)
        img = Image.open(io.BytesIO(image_data)).convert("RGB")

        results = yolo_model.predict(img, conf=0.3)

        clothing_tensors = []
        detected_labels = []

        for result in results:
            for box, cls in zip(result.boxes.xyxy, result.boxes.cls):
                label = yolo_model.names[int(cls)]
                detected_labels.append(label)
                if label in CLOTHING_CLASSES:
                    x1, y1, x2, y2 = map(int, box.tolist())
                    crop = img.crop((x1, y1, x2, y2))
                    tensor = preprocess(crop).unsqueeze(0)
                    clothing_tensors.append(tensor)

        _logger.info(f"Vêtements détectés dans l'image : {detected_labels}")

        if not clothing_tensors:
            raise ValidationError("Aucun vêtement détecté dans l'image.")

        return clothing_tensors

    def compare_with_products(self):
        for record in self:
            if not record.image_1:
                raise ValidationError("L'image 1 est requise pour la comparaison.")

            try:
                model, preprocess, _ = self._get_models()
                tensors = record._extract_clothing_tensors(record.image_1)

                with torch.no_grad():
                    vecs = [model.encode_image(t).cpu().numpy() for t in tensors]

                mean_vec = np.mean(np.vstack(vecs), axis=0)

                products = self.env['product.template'].search([('clip_vector', '!=', False)])
                scored_products = []

                for prod in products:
                    try:
                        vec_bytes = base64.b64decode(prod.clip_vector)
                        prod_vec = pickle.loads(vec_bytes)
                        score = np.dot(mean_vec.flatten(), prod_vec.flatten()) / (
                            np.linalg.norm(mean_vec) * np.linalg.norm(prod_vec)
                        )
                        if score >= 0.8:
                            scored_products.append((prod, score))
                    except Exception as e:
                        _logger.warning(f"Erreur produit {prod.name}: {e}")
                        continue

                if not scored_products:
                    raise ValidationError("❌ Aucun produit avec une similarité de 80 % ou plus trouvé.")

                # Trier par score décroissant
                scored_products.sort(key=lambda x: x[1], reverse=True)

                record.similarity_score = scored_products[0][1]
                record.name = f"Ressemble à : {scored_products[0][0].name} ({round(scored_products[0][1] * 100, 2)}%)"

                # Supprimer anciennes lignes et recréer les nouvelles avec score
                record.matched_product_line_ids.unlink()
                lines = []
                for prod, score in scored_products:
                    lines.append((0, 0, {
                        'product_id': prod.id,
                        'clip_similarity_score': round(score * 100, 2),
                    }))
                record.matched_product_line_ids = lines

            except Exception as e:
                raise ValidationError(f"Erreur de comparaison : {str(e)}")

    @api.depends("similarity_score")
    def _compute_similarity_display(self):
        for rec in self:
            percent = round(rec.similarity_score * 100, 2)
            if percent >= 80:
                color = "green"
            elif percent >= 50:
                color = "orange"
            else:
                color = "red"
            rec.similarity_display = f"<span style='color:{color}; font-weight:bold'>{percent} %</span>"
