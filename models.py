from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # Could add user info here if we had auth

class RiskEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable=False)
    
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
    risk_level = db.Column(db.Integer) # 1-5
    
    assessment = db.relationship('Assessment', backref=db.backref('entries', lazy=True))
