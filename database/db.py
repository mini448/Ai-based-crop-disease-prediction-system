import sqlite3
import os

class Database:
    def __init__(self, db_path=None):
        self.db_path = db_path or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'crop_disease.db')
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        conn = self.get_connection()
        schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema.sql')
        with open(schema_path, 'r', encoding='utf-8-sig') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
    
    def create_user(self, username, email, password_hash):
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            cur.execute('INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                        (username, email, password_hash))
            conn.commit()
            user_id = cur.lastrowid
            return user_id
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    def get_user_by_username(self, username):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cur.fetchone()
        conn.close()
        return user
    
    def get_user_by_email(self, email):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cur.fetchone()
        conn.close()
        return user
    
    def save_prediction(self, user_id, image_path, crop_name, predicted_disease, confidence):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO predictions (user_id, image_path, crop_name, predicted_disease, confidence) VALUES (?, ?, ?, ?, ?)',
                    (user_id, image_path, crop_name, predicted_disease, confidence))
        conn.commit()
        pred_id = cur.lastrowid
        conn.close()
        return pred_id
    
    def get_user_predictions(self, user_id, limit=None):
        conn = self.get_connection()
        cur = conn.cursor()
        query = 'SELECT * FROM predictions WHERE user_id = ? ORDER BY created_at DESC'
        params = [user_id]
        if limit:
            query += ' LIMIT ?'
            params.append(int(limit))
        cur.execute(query, params)
        predictions = cur.fetchall()
        conn.close()
        return predictions
    
    def get_prediction_by_id(self, pred_id, user_id):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM predictions WHERE id = ? AND user_id = ?', (pred_id, user_id))
        prediction = cur.fetchone()
        conn.close()
        return prediction
    
    def get_disease_info(self, crop_name, disease_name):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM disease_info WHERE crop_name = ? AND disease_name = ?', (crop_name, disease_name))
        info = cur.fetchone()
        if not info:
            # fallback by disease name only
            cur.execute('SELECT * FROM disease_info WHERE disease_name = ? LIMIT 1', (disease_name,))
            info = cur.fetchone()
        conn.close()
        return info
    
    def get_analytics(self, user_id):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) as total FROM predictions WHERE user_id = ?', (user_id,))
        total = cur.fetchone()['total']
        cur.execute("SELECT COUNT(*) as healthy FROM predictions WHERE user_id = ? AND lower(predicted_disease) LIKE '%healthy%'", (user_id,))
        healthy = cur.fetchone()['healthy']
        diseased = total - healthy
        cur.execute('''SELECT predicted_disease, COUNT(*) as count FROM predictions 
                       WHERE user_id = ? GROUP BY predicted_disease ORDER BY count DESC LIMIT 5''', (user_id,))
        top_diseases = cur.fetchall()
        cur.execute('SELECT * FROM predictions WHERE user_id = ? ORDER BY created_at DESC LIMIT 5', (user_id,))
        recent = cur.fetchall()
        conn.close()
        return {
            'total': total,
            'healthy': healthy,
            'diseased': diseased,
            'top_diseases': top_diseases,
            'recent': recent
        }

if __name__ == '__main__':
    db = Database()
    db.init_db()
    print('Database initialized')
