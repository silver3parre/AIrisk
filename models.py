from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Draft') # Draft, Completed
    
    # Scoping Data (Suggestion 10)
    title = db.Column(db.String(200), default='Untitled Assessment')
    security_categorization = db.Column(db.String(50)) # Low, Moderate, High
    description = db.Column(db.Text)
    
    # User Info (Suggestion 9)
    created_by = db.Column(db.String(100)) # Username

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    asset_type = db.Column(db.String(100))  # Hardware, Software, Data, etc.
    valuation = db.Column(db.Float, nullable=True)  # Optional asset value
    
    assessment = db.relationship('Assessment', backref=db.backref('assets', lazy=True))

class RiskEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable=False)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=True)
    
    threat_source = db.Column(db.String(200))
    threat_event = db.Column(db.String(200))
    
    # Adversarial Factors (Table I-4)
    capability = db.Column(db.String(100))
    intent = db.Column(db.String(100))
    targeting = db.Column(db.String(100))
    
    vulnerability = db.Column(db.String(200))
    
    likelihood_initiation = db.Column(db.Integer) # 1-5
    likelihood_impact = db.Column(db.Integer) # 1-5
    overall_likelihood = db.Column(db.Integer) # 1-5
    
    impact_level = db.Column(db.Integer) # 1-5
    financial_impact = db.Column(db.Float, nullable=True)  # CRQ: Estimated loss in $
    risk_level = db.Column(db.Integer) # 1-5
    
    assessment = db.relationship('Assessment', backref=db.backref('entries', lazy=True))
    asset = db.relationship('Asset', backref=db.backref('risk_entries', lazy=True))
