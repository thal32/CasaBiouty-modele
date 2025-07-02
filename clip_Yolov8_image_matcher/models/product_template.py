from odoo import models, fields, api
from odoo.exceptions import UserError
import torch
import clip
from PIL import Image, UnidentifiedImageError
import io
import base64 as b64
import numpy as np
import pickle
import logging

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    clip_vector = fields.Binary("Vecteur CLIP", copy=False)

    def generate_clip_vector(self):
        """Génère et stocke le vecteur CLIP à partir de l'image principale du produit"""
        model, preprocess = self._get_clip_model()

        if not self.image_1920:
            raise UserError("🚫 Le produit n’a pas d’image principale. Veuillez en ajouter une.")

        try:
            image_data = b64.b64decode(self.image_1920)

            # Vérifier si l'image est décodable
            try:
                img = Image.open(io.BytesIO(image_data)).convert("RGB")
            except UnidentifiedImageError:
                raise UserError("❌ L’image du produit est invalide ou corrompue.")

            tensor = preprocess(img).unsqueeze(0)

            with torch.no_grad():
                vec = model.encode_image(tensor).cpu().numpy()

            # Ne stocke que dans clip_vector (pas besoin de clip_vector_np)
            self.clip_vector = b64.b64encode(pickle.dumps(vec)).decode('utf-8')

            self.message_post(body="✅ Vecteur CLIP généré avec succès.", message_type='notification')

        except Exception as e:
            _logger.exception("Erreur lors de la génération du vecteur CLIP")
            raise UserError(f"❌ Erreur lors de la génération du vecteur CLIP : {str(e)}")

    @api.model
    def _get_clip_model(self):
        if not hasattr(self.env, "_clip_model"):
            self.env._clip_model, self.env._clip_preprocess = clip.load("ViT-B/32", device="cpu")
            self.env._clip_model.eval()
        return self.env._clip_model, self.env._clip_preprocess
