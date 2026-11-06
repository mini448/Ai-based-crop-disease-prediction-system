from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from werkzeug.utils import secure_filename
import os, json
from datetime import datetime
from database.db import Database
from ml_model.predict import DiseasePredictor
from services.recommendation import RecommendationEngine

prediction_bp = Blueprint('prediction', __name__)
db = Database()
recommender = RecommendationEngine()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

def _model_is_demo():
    meta = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ml_model', 'saved_model', 'model_metadata.json')
    try:
        if os.path.exists(meta):
            with open(meta) as f:
                return bool(json.load(f).get('is_demo_dataset'))
    except Exception:
        pass
    # fallback: detect demo training images in dataset
    ds = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'dataset')
    demo = real = 0
    if os.path.isdir(ds):
        for root, _, files in os.walk(ds):
            for fn in files:
                if fn.lower().endswith(('.jpg','.jpeg','.png')):
                    if '_demo' in fn.lower(): demo += 1
                    else: real += 1
    return demo > 0 and real == 0

@prediction_bp.route('/detect', methods=['GET', 'POST'])
def detect():
    if 'user_id' not in session:
        flash('Please login to access this page', 'warning')
        return redirect(url_for('auth.login'))
    model_demo = _model_is_demo()
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            try:
                predictor = DiseasePredictor()
                result = predictor.predict(filepath)
                db.save_prediction(session['user_id'], f'static/uploads/{filename}', result['crop_name'], result['disease_name'], result['confidence'])
                recommendations = recommender.get_recommendations(result['disease_name'], result['crop_name'])
                disease_info = db.get_disease_info(result['crop_name'], result['disease_name'])
                return render_template('result.html', result=result, recommendations=recommendations, disease_info=disease_info, image_path=f'static/uploads/{filename}')
            except FileNotFoundError as e:
                if os.path.exists(filepath):
                    try: os.remove(filepath)
                    except OSError: pass
                flash(str(e), 'warning')
                return redirect(request.url)
            except Exception as e:
                flash(f'Error during prediction: {str(e)}', 'danger')
                return redirect(request.url)
        else:
            flash('Invalid file type. Please upload JPG, JPEG, or PNG files only.', 'danger')
            return redirect(request.url)
    return render_template('detect.html', model_demo=model_demo)

@prediction_bp.route('/history')
def history():
    if 'user_id' not in session:
        flash('Please login to access this page', 'warning')
        return redirect(url_for('auth.login'))
    predictions = db.get_user_predictions(session['user_id'])
    return render_template('history.html', predictions=predictions)

@prediction_bp.route('/result/<int:pred_id>')
def view_result(pred_id):
    if 'user_id' not in session:
        flash('Please login to access this page', 'warning')
        return redirect(url_for('auth.login'))
    prediction = db.get_prediction_by_id(pred_id, session['user_id'])
    if not prediction:
        flash('Prediction not found', 'danger')
        return redirect(url_for('prediction.history'))
    disease_info = db.get_disease_info(prediction['crop_name'], prediction['predicted_disease'])
    return render_template('view_result.html', prediction=prediction, disease_info=disease_info)
