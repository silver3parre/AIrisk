import unittest
import os
import sys
import io
import json

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import Assessment

class TestFeatures(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False # Disable CSRF for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        
        with app.app_context():
            db.create_all()
            
        # Login as Analyst
        with self.client.session_transaction() as sess:
            sess['user_role'] = 'Analyst'
            sess['username'] = 'testuser'
            
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_dashboard_empty(self):
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No assessments found', response.data)

    def test_save_assessment(self):
        with self.client.session_transaction() as sess:
            sess['assessment_data'] = {
                'asset_name': 'Test Asset',
                'asset_type': 'Data',
                'risk_level': 3
            }
        
        response = self.client.post('/assessment/save', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)
        self.assertIn(b'Test Asset', response.data)
        
        with app.app_context():
            self.assertEqual(Assessment.query.count(), 1)

    def test_vulnerability_upload(self):
        # Mock file content
        data = {
            'vulnerability': 'SQL Injection',
            'threat_event': 'Database Compromise'
        }
        json_file = (io.BytesIO(json.dumps(data).encode('utf-8')), 'scan.json')
        
        # Step 8 is where upload happens, but logic is in assessment_step generic handler
        # We need to simulate being on step 8 or just posting to it
        with self.client.session_transaction() as sess:
            sess['assessment_data'] = {}
            
        response = self.client.post('/assessment/step/8', data={
            'vulnerability_report': json_file,
            'vulnerability': 'Manual Input' # Required field, but file should overwrite or be processed
        }, content_type='multipart/form-data', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        
        # Check if session data was updated
        with self.client.session_transaction() as sess:
            self.assertEqual(sess['assessment_data'].get('vulnerability'), 'SQL Injection')
            self.assertEqual(sess['assessment_data'].get('threat_event'), 'Database Compromise')

if __name__ == '__main__':
    unittest.main()
