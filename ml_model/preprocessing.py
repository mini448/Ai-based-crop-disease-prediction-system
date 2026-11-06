import cv2
import numpy as np
from PIL import Image

def preprocess_image_for_model(image_path, target_size=(224, 224)):
    # Read image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Resize
    img = cv2.resize(img, target_size)
    # Normalize
    img = img.astype(np.float32) / 255.0
    # Add batch dimension
    img = np.expand_dims(img, axis=0)
    return img

def enhance_image(image_path):
    img = cv2.imread(image_path)
    # Apply Gaussian blur to reduce noise
    img = cv2.GaussianBlur(img, (3, 3), 0)
    return img
