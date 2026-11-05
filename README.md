# AI-Based Crop Disease Prediction and Recommendation System

## Project Overview
Complete Flask web application for detecting crop diseases using Machine Learning and Computer Vision (MobileNetV2 transfer learning). This workspace is configured to use the **PlantVillage 100-Image Setup** dataset (Tomato, 5 classes, 20 images each) located in PlantVillage_100_Image_Setup/.

> **Important:** The 100-image subset is for demo/academic training only and is **not** sufficient for reliable real-world diagnosis. For real results, train on the full PlantVillage dataset (or a larger, field-collected dataset) and report metrics from that evaluation.

## Features
- User authentication (register/login, password hashing)
- Image upload (JPG/JPEG/PNG) with preview and validation
- AI disease detection (MobileNetV2) with confidence and top predictions
- Low-confidence warning
- Disease information (symptoms, causes, prevention, guidance)
- AI recommendation engine (preventive guidance; no chemical/pesticide prescriptions)
- Prediction history and per-result reports
- Analytics dashboard (Chart.js)
- SQLite database

## Supported Classes (100-Image Tomato Subset)
- Tomato___Bacterial_spot
- Tomato___Early_blight
- Tomato___Late_blight
- Tomato___Leaf_Mold
- Tomato___healthy

## Technology Stack
- Frontend: HTML5, CSS3, JavaScript, Bootstrap 5, Chart.js
- Backend: Python, Flask
- ML: TensorFlow/Keras (MobileNetV2), OpenCV, NumPy, Pandas, scikit-learn
- Database: SQLite

## Setup (Windows / PowerShell)
From D:\crop disease:

`powershell
# 1) Activate venv (already present in this workspace) or create one
# python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2) Install dependencies
pip install -r requirements.txt

# 3) Create the 100-image dataset (requires internet; TFDS downloads source data)
cd PlantVillage_100_Image_Setup
pip install tensorflow-datasets pillow
python create_100_dataset.py
cd ..

# 4) Train and evaluate the model (uses ./dataset created above)
python -m ml_model.train_model

# 5) Run the web app
python app.py
`

Open http://localhost:5000

## Training Outputs (generated, not hardcoded)
After training, ml_model/saved_model/ contains:
- crop_disease_model.h5
- class_indices.json
- confusion_matrix.png

The training script prints accuracy/precision/recall/F1 and a confusion matrix from the evaluation split. **Report the actual metrics produced by your run**; do not copy example numbers.

## Project Structure
`
crop_disease_prediction/
├── app.py
├── config.py
├── requirements.txt
├── ml_model/
│   ├── train_model.py
│   ├── predict.py
│   ├── preprocessing.py
│   └── saved_model/
├── dataset/                      # created by PlantVillage_100_Image_Setup
├── PlantVillage_100_Image_Setup/ # 100-image subset builder
├── database/
│   ├── db.py
│   └── schema.sql
├── routes/
├── services/
├── templates/
├── static/
└── README.md
`

## Notes & Safety
- Predictions can be uncertain; the UI shows confidence and a low-confidence warning.
- Recommendations are general/preventive guidance and **do not replace agricultural experts**.
- Uploaded files are validated (type/size) and stored with safe server-generated names.
- No secrets are committed; set SECRET_KEY via environment for production.

## Troubleshooting
- **Model not found**: run python -m ml_model.train_model after preparing dataset/.
- **Dataset empty**: run PlantVillage_100_Image_Setup/create_100_dataset.py (internet required on first TFDS download).
- **Dependency conflicts**: this workspace uses an existing .venv; if recreating, prefer a fresh venv and compatible TensorFlow/protobuf versions for your platform.
