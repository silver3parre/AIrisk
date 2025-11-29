from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, Assessment, RiskEntry, Asset
import os
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from functools import wraps
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

# RBAC Decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_role' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_role' not in session:
                return redirect(url_for('login'))
            if session['user_role'] not in allowed_roles:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        role = request.form.get('role')
        
        if username and role:
            session['username'] = username
            session['user_role'] = role
            flash(f'Welcome, {username}! Logged in as {role}.', 'success')
            return redirect(url_for('index'))
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

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
@login_required
def about():
    return render_template('about.html')

@app.route('/assessment/start')
@login_required
@role_required(['Analyst', 'Admin'])
def start_assessment():
    # Redirect to Scoping first (Suggestion 10)
    return redirect(url_for('assessment_scope'))

@app.route('/assessment/scope', methods=['GET', 'POST'])
@login_required
@role_required(['Analyst', 'Admin'])
def assessment_scope():
    if request.method == 'POST':
        # Don't clear the whole session, just reset assessment data
        session.pop('assessment_data', None)
        session.pop('step', None)
        
        session['assessment_data'] = {}
        session['step'] = 1
        
        # Save Scope Data to Session
        session['assessment_data']['title'] = request.form.get('assessment_title')
        session['assessment_data']['security_categorization'] = request.form.get('security_categorization')
        session['assessment_data']['description'] = request.form.get('system_description')
        
        return redirect(url_for('assessment_step', step_id=1))
        
    return render_template('scope.html')

@app.route('/assessment/step/<int:step_id>', methods=['GET', 'POST'])
@login_required
@role_required(['Analyst', 'Admin'])
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
            
        # Handle File Upload (Step 8 is where we added it, but it submits with the form)
        if 'vulnerability_report' in request.files:
            file = request.files['vulnerability_report']
            if file and file.filename != '':
                from vulnerability_parser import parse_vulnerability_report
                import os
                
                filename = file.filename
                ext = os.path.splitext(filename)[1].lower()
                
                # Parse the file
                parsed_data = parse_vulnerability_report(file, ext)
                
                if parsed_data:
                    # Update session data with parsed values
                    # We might want to overwrite or only fill if empty. 
                    # Let's overwrite as the user explicitly uploaded a file.
                    for key, value in parsed_data.items():
                        if value:
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
@login_required
def assessment_result():
    data = session.get('assessment_data', {})
    # Here we would calculate the risk
    # For now, just render the template
    from risk_logic import calculate_risk_details
    
    risk_details = calculate_risk_details(data)
    
    return render_template('result.html', risk=risk_details)

@app.route('/dashboard')
@login_required
def dashboard():
    assessments = Assessment.query.order_by(Assessment.date_created.desc()).all()
    return render_template('dashboard.html', assessments=assessments)

@app.route('/assessment/save', methods=['POST'])
@login_required
@role_required(['Analyst', 'Admin'])
def save_assessment():
    data = session.get('assessment_data')
    if not data:
        return redirect(url_for('index'))
    
    # Create Assessment
    assessment = Assessment(
        status='Completed',
        title=data.get('title', 'Untitled Assessment'),
        security_categorization=data.get('security_categorization'),
        description=data.get('description'),
        created_by=session.get('username')
    )
    # Explicitly set title to ensure it's not overwritten by default
    if data.get('title'):
        assessment.title = data.get('title')
        
    db.session.add(assessment)
    db.session.flush() # Get ID
    
    # Create Asset
    asset = Asset(
        assessment_id=assessment.id,
        name=data.get('asset_name', 'Unknown Asset'),
        asset_type=data.get('asset_type'),
        valuation=data.get('asset_valuation')
    )
    db.session.add(asset)
    
    # Create Risk Entry
    from risk_logic import calculate_overall_likelihood, calculate_risk
    
    l_init = int(data.get('likelihood_initiation', 1))
    l_impact = int(data.get('likelihood_impact', 1))
    impact = int(data.get('impact_level', 1))
    
    overall_likelihood = calculate_overall_likelihood(l_init, l_impact)
    risk_score = calculate_risk(overall_likelihood, impact)
    
    risk_entry = RiskEntry(
        assessment_id=assessment.id,
        asset_id=asset.id, # Will be linked after flush/commit
        threat_source=data.get('threat_source'),
        threat_event=data.get('threat_event'),
        capability=data.get('capability'),
        intent=data.get('intent'),
        targeting=data.get('targeting'),
        vulnerability=data.get('vulnerability'),
        likelihood_initiation=l_init,
        likelihood_impact=l_impact,
        overall_likelihood=overall_likelihood,
        impact_level=impact,
        financial_impact=data.get('financial_impact'),
        risk_level=risk_score
    )
    db.session.add(risk_entry)
    db.session.commit()
    
    # Clear Assessment Data from Session
    session.pop('assessment_data', None)
    session.pop('step', None)
    
    return redirect(url_for('dashboard'))

@app.route('/assessment/delete/<int:assessment_id>', methods=['POST'])
@login_required
@role_required(['Admin'])
def delete_assessment(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    
    # Delete associated assets and risk entries
    RiskEntry.query.filter_by(assessment_id=assessment.id).delete()
    Asset.query.filter_by(assessment_id=assessment.id).delete()
    
    db.session.delete(assessment)
    db.session.commit()
    flash('Assessment deleted successfully.', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    # Security Fix: Disable debug mode in production
    app.run(debug=False)
