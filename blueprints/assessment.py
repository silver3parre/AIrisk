from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from decorators import login_required, role_required
from models import db, Assessment, RiskEntry, Asset
from risk_logic import calculate_risk_details, persist_assessment

assessment_bp = Blueprint('assessment', __name__, url_prefix='/assessment')

@assessment_bp.route('/start')
@login_required
@role_required(['Analyst', 'Admin'])
def start_assessment():
    return render_template('assessment_selection.html')

@assessment_bp.route('/scope', methods=['GET', 'POST'])
@login_required
@role_required(['Analyst', 'Admin'])
def assessment_scope():
    if request.method == 'POST':
        session.pop('assessment_data', None)
        session.pop('step', None)
        
        session['assessment_data'] = {}
        session['step'] = 1
        
        session['assessment_data']['title'] = request.form.get('assessment_title')
        session['assessment_data']['security_categorization'] = request.form.get('security_categorization')
        session['assessment_data']['description'] = request.form.get('system_description')
        
        return redirect(url_for('assessment.assessment_step', step_id=1))
        
    return render_template('scope.html')

@assessment_bp.route('/step/<int:step_id>', methods=['GET', 'POST'])
@login_required
@role_required(['Analyst', 'Admin'])
def assessment_step(step_id):
    if request.method == 'POST':
        data = request.form
        if 'assessment_data' not in session:
            session['assessment_data'] = {}
        
        current_data = session['assessment_data']
        for key, value in data.items():
            current_data[key] = value
            
        if 'vulnerability_report' in request.files:
            file = request.files['vulnerability_report']
            if file and file.filename != '':
                from vulnerability_parser import parse_vulnerability_report
                import os
                filename = file.filename
                ext = os.path.splitext(filename)[1].lower()
                parsed_data = parse_vulnerability_report(file, ext)
                if parsed_data:
                    for key, value in parsed_data.items():
                        if value:
                            current_data[key] = value
                            
        session['assessment_data'] = current_data
        
        next_step = step_id + 1
        if next_step > 11:
            return redirect(url_for('assessment.assessment_result'))
        return redirect(url_for('assessment.assessment_step', step_id=next_step))
    
    suggested_threats = []
    if step_id == 3:
        from threat_intel import get_suggested_threats
        asset_type = session.get('assessment_data', {}).get('asset_type')
        if asset_type:
            suggested_threats = get_suggested_threats(asset_type)

    return render_template('assessment_wizard.html', step=step_id, suggested_threats=suggested_threats)

@assessment_bp.route('/result')
@login_required
def assessment_result():
    data = session.get('assessment_data', {})
    risk_details = calculate_risk_details(data)
    return render_template('result.html', risk=risk_details)

@assessment_bp.route('/view/<int:assessment_id>')
@login_required
def view_assessment(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    return render_template('view_assessment.html', assessment=assessment)

@assessment_bp.route('/save', methods=['POST'])
@login_required
@role_required(['Analyst', 'Admin'])
def save_assessment():
    data = session.get('assessment_data')
    if not data:
        return redirect(url_for('main.index'))
    
    persist_assessment(data, session.get('username'))
    
    session.pop('assessment_data', None)
    session.pop('step', None)
    
    return redirect(url_for('main.dashboard'))

@assessment_bp.route('/delete/<int:assessment_id>', methods=['POST'])
@login_required
@role_required(['Admin'])
def delete_assessment(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    RiskEntry.query.filter_by(assessment_id=assessment.id).delete()
    Asset.query.filter_by(assessment_id=assessment.id).delete()
    db.session.delete(assessment)
    db.session.commit()
    
    if request.headers.get('HX-Request'):
        return ''
        
    flash('Assessment deleted successfully.', 'success')
    return redirect(url_for('main.dashboard'))
