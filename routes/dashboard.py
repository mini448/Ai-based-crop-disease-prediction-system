from flask import Blueprint, render_template, session, redirect, url_for, flash
from database.db import Database

dashboard_bp = Blueprint('dashboard', __name__)
db = Database()

@dashboard_bp.route('/dashboard')
def index():
    if 'user_id' not in session:
        flash('Please login to access this page', 'warning')
        return redirect(url_for('auth.login'))
    
    analytics = db.get_analytics(session['user_id'])
    return render_template('dashboard.html', analytics=analytics, username=session['username'])

@dashboard_bp.route('/analytics')
def analytics():
    if 'user_id' not in session:
        flash('Please login to access this page', 'warning')
        return redirect(url_for('auth.login'))
    
    analytics_data = db.get_analytics(session['user_id'])
    return render_template('analytics.html', analytics=analytics_data)
