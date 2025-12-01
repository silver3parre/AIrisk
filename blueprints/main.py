from flask import Blueprint, render_template
from decorators import login_required
from models import Assessment

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/about')
@login_required
def about():
    return render_template('about.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    assessments = Assessment.query.order_by(Assessment.date_created.desc()).all()
    return render_template('dashboard.html', assessments=assessments)
