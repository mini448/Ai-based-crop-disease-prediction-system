import os
import json
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image

class DiseasePredictor:
    def __init__(self, model_path=None, class_indices_path=None):
        from config import Config
        self.model_path = model_path or Config.MODEL_PATH
        self.class_indices_path = class_indices_path or Config.CLASS_INDICES_PATH
        self.metadata_path = os.path.join(os.path.dirname(self.model_path), 'model_metadata.json')
        self.model = None
        self.class_indices = None
        self.class_names = None
        self.metadata = {}
        self.load_model_and_classes()
    
    def load_model_and_classes(self):
        if os.path.exists(self.model_path):
            self.model = load_model(self.model_path)
        else:
            raise FileNotFoundError(
                f'Model not found at {self.model_path}. Train the model first (run PlantVillage_100_Image_Setup/create_100_dataset.py then python -m ml_model.train_model).'
            )
        if os.path.exists(self.class_indices_path):
            with open(self.class_indices_path, 'r') as f:
                self.class_indices = json.load(f)
            self.class_names = {int(v): k for k, v in self.class_indices.items()}
        else:
            raise FileNotFoundError(f'Class indices not found at {self.class_indices_path}.')
        if os.path.exists(self.metadata_path):
            try:
                with open(self.metadata_path, 'r') as f:
                    self.metadata = json.load(f)
            except Exception:
                self.metadata = {}
    
    def preprocess_image(self, image_path, target_size=(224, 224)):
        img = Image.open(image_path).convert('RGB')
        img = img.resize(target_size)
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0
        return img_array
    
    def predict(self, image_path):
        processed_image = self.preprocess_image(image_path)
        predictions = self.model.predict(processed_image, verbose=0)
        predicted_class_idx = int(np.argmax(predictions[0]))
        confidence = float(predictions[0][predicted_class_idx])
        predicted_class = self.class_names[predicted_class_idx]
        
        top_indices = np.argsort(predictions[0])[::-1][:3]
        top_predictions = [{'class': self.class_names[int(idx)], 'confidence': float(predictions[0][idx])} for idx in top_indices]
        
        if '___' in predicted_class:
            parts = predicted_class.split('___', 1)
            crop_name = parts[0].replace('_', ' ')
            disease_name = parts[1]
        elif 'healthy' in predicted_class.lower():
            crop_name = predicted_class.replace('___', ' ').replace('_', ' ').replace('healthy', '').strip() or 'Tomato'
            disease_name = 'healthy'
        else:
            parts = predicted_class.split('_', 1)
            crop_name = parts[0].replace('_', ' ')
            disease_name = parts[1] if len(parts) > 1 else predicted_class
        
        is_demo = bool(self.metadata.get('is_demo_dataset'))
        return {
            'predicted_class': predicted_class,
            'crop_name': crop_name,
            'disease_name': disease_name,
            'confidence': confidence,
            'top_predictions': top_predictions,
            'is_healthy': 'healthy' in predicted_class.lower(),
            'low_confidence': confidence < 0.6,
            'model_warning': (
                'This model was trained on synthetic demo placeholder images, not real PlantVillage leaf photos. '
                'Predictions for real/diseased leaves may be incorrect (including false “healthy”). '
                'Run PlantVillage_100_Image_Setup/create_100_dataset.py to download real images, then retrain with: python -m ml_model.train_model'
            ) if is_demo else None,
            'model_metadata': self.metadata,
        }
