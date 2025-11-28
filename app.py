from flask import Flask, render_template, request, redirect, url_for, session
from models import db, Assessment, RiskEntry
import os
from flask_wtf.csrf import CSRFProtect

from flask_migrate import Migrate

import logging
from logging.config import dictConfig

# Configure logging
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
# Security Configuration
if os.environ.get('FLASK_ENV') == 'production':
    if not os.environ.get('SECRET_KEY'):
        raise ValueError("No SECRET_KEY set for production configuration")
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
else:
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-prod')
    app.config['SESSION_COOKIE_SECURE'] = False
    app.config['SESSION_COOKIE_HTTPONLY'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///risk_assessment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

csrf = CSRFProtect(app)

db.init_app(app)
migrate = Migrate(app, db)


@app.after_request
def add_security_headers(response):
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/assessment/start')
def start_assessment():
    # Create a new assessment session
    # For simplicity in this guided flow, we might just use session storage 
    # or create a DB entry immediately. Let's use session for the wizard state.
    session.clear()
    session['step'] = 1
    session['assessment_data'] = {}
    return redirect(url_for('assessment_step', step_id=1))

@app.route('/assessment/step/<int:step_id>', methods=['GET', 'POST'])
def assessment_step(step_id):
    if request.method == 'POST':
        # Save data from current step
        data = request.form
        if 'assessment_data' not in session:
            session['assessment_data'] = {}
        
        # Update session data
        current_data = session['assessment_data']
        for key, value in data.items():
            current_data[key] = value
        session['assessment_data'] = current_data
        
        next_step = step_id + 1
        if next_step > 11: # Updated to 11 steps: Asset + 10 original steps
            return redirect(url_for('assessment_result'))
        return redirect(url_for('assessment_step', step_id=next_step))
    
    # Threat Intel Integration
    suggested_threats = []
    if step_id == 3:
        from threat_intel import get_suggested_threats
        asset_type = session.get('assessment_data', {}).get('asset_type')
        if asset_type:
            suggested_threats = get_suggested_threats(asset_type)

    return render_template('assessment_wizard.html', step=step_id, suggested_threats=suggested_threats)

@app.route('/assessment/result')
def assessment_result():
    data = session.get('assessment_data', {})
    # Here we would calculate the risk
    # For now, just render the template
    from risk_logic import calculate_risk_details
    
    risk_details = calculate_risk_details(data)
    
    return render_template('result.html', risk=risk_details)

if __name__ == '__main__':
    # Security Fix: Disable debug mode in production
    app.run(debug=False)
