# Improved dataset creation: saves to project dataset, handles missing classes gracefully
from pathlib import Path
from collections import defaultdict
import os
import tensorflow_datasets as tfds
from PIL import Image

TARGET_CLASSES = [
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___healthy",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
]
PER_CLASS = 20
PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT = PROJECT_ROOT / "dataset"
OUT.mkdir(exist_ok=True)

print(f"Output: {OUT}")
print("Loading PlantVillage via TensorFlow Datasets (may download on first run)...")
builder = tfds.builder("plant_village")
builder.download_and_prepare()
ds = builder.as_dataset(split="train", shuffle_files=True)
label_names = builder.info.features["label"].names
counts = defaultdict(int)

for example in tfds.as_numpy(ds):
    label_id = int(example["label"])
    class_name = label_names[label_id]
    if class_name not in TARGET_CLASSES or counts[class_name] >= PER_CLASS:
        continue
    class_dir = OUT / class_name
    class_dir.mkdir(parents=True, exist_ok=True)
    # remove demo placeholders if present
    for p in class_dir.glob('*_demo.jpg'):
        try: p.unlink()
        except: pass
    image = Image.fromarray(example["image"]).convert("RGB")
    n = counts[class_name] + 1
    image.save(class_dir / f"{class_name}_{n:03d}.jpg", quality=92)
    counts[class_name] = n
    print(f"{class_name}: {n}/{PER_CLASS}")
    if all(counts.get(name,0) >= PER_CLASS for name in TARGET_CLASSES):
        break

print("\nResult:")
for name in TARGET_CLASSES:
    print(f"  {name}: {counts.get(name,0)}")
total = sum(counts.get(n,0) for n in TARGET_CLASSES)
if total == 100:
    print(f"SUCCESS: 100 images saved to {OUT}")
else:
    print(f"WARNING: saved {total} images (expected 100). Check internet/TFDS cache and rerun.")
