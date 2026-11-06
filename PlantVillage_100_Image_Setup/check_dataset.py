# Create dataset structure for the 5 Tomato classes (100-image subset)
import os
from PIL import Image
import numpy as np

base = r"D:\crop disease\dataset"
classes = [
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___healthy",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
]

# Only create placeholders if empty - user may have real images
for cls in classes:
    d = os.path.join(base, cls)
    os.makedirs(d, exist_ok=True)

# Check counts
for cls in classes:
    d = os.path.join(base, cls)
    n = len([f for f in os.listdir(d) if f.lower().endswith(('.jpg','.jpeg','.png'))])
    print(f"{cls}: {n}")
