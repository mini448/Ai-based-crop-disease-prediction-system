CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    image_path TEXT NOT NULL,
    crop_name TEXT NOT NULL,
    predicted_disease TEXT NOT NULL,
    confidence REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS disease_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    crop_name TEXT NOT NULL,
    disease_name TEXT NOT NULL,
    symptoms TEXT,
    causes TEXT,
    prevention TEXT,
    treatment_guidance TEXT
);

INSERT OR IGNORE INTO disease_info (crop_name, disease_name, symptoms, causes, prevention, treatment_guidance) VALUES
('Tomato', 'Bacterial_spot', 'Small, dark brown spots with yellow halos on leaves. Spots may appear on stems and fruits.', 'Bacteria spread through water splash, contaminated tools, and infected seeds.', 'Use certified disease-free seeds, avoid overhead watering, practice crop rotation, remove infected plant debris.', 'Remove infected plants. Use copper-based bactericides as a last resort. Consult agricultural experts for chemical treatment options.'),
('Tomato', 'Early_blight', 'Dark brown spots with concentric rings on lower leaves. Yellowing around spots.', 'Fungus Alternaria solani. Favored by warm, humid conditions and plant stress.', 'Rotate crops every 2-3 years, stake plants for air circulation, mulch to prevent soil splash, remove lower leaves.', 'Remove affected leaves. Apply fungicides preventively. Maintain proper plant spacing and nutrition.'),
('Tomato', 'Late_blight', 'Water-soaked gray spots on leaves, white mold on undersides. Rapid spreading in cool wet weather.', 'Phytophthora infestans. Spreads rapidly in cool, wet conditions.', 'Plant resistant varieties, ensure good drainage, avoid overhead irrigation, destroy infected plants.', 'Act quickly - remove and destroy infected plants. Apply appropriate fungicides. Monitor weather conditions.'),
('Tomato', 'Leaf_Mold', 'Yellow patches on upper leaf surfaces, olive-green mold on undersides.', 'Fungus Passalora fulva. Thrives in high humidity and poor air circulation.', 'Improve ventilation, reduce humidity, avoid wetting foliage, space plants properly.', 'Improve air circulation. Remove infected leaves. Apply fungicides if severe.'),
('Tomato', 'healthy', 'Healthy green leaves with no spots, discoloration, or damage.', 'N/A', 'Maintain proper watering, fertilization, pest control, and good cultural practices.', 'No treatment needed. Continue good agricultural practices.');
