import unittest
from app import app, db
from models import Assessment, RiskEntry

class TestIntegration(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_full_assessment_flow(self):
        """Test the complete assessment wizard flow."""
        # 0. Login
        self.app.post('/login', data={'username': 'testuser', 'role': 'Analyst'}, follow_redirects=True)

        # 1. Start Assessment -> Selection -> Scope
        self.app.get('/assessment/start', follow_redirects=True)
        
        # 2. Submit Scope (New Step)
        response = self.app.post('/assessment/scope', data={
            'assessment_title': 'Integration Test',
            'security_categorization': 'High',
            'system_description': 'Test System'
        }, follow_redirects=True)
        
        self.assertIn(b'Step 1', response.data)

        # 2. Submit Step 1 (Asset Identification) [NEW]
        response = self.app.post('/assessment/step/1', data={
            'asset_name': 'Customer DB',
            'asset_type': 'Data',
            'asset_valuation': '100000'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Step 2', response.data)

        # 3. Submit Step 2 (Threat Source) [Formerly Step 1]
        response = self.app.post('/assessment/step/2', data={'threat_source': 'External Hacker'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Step 3', response.data)

        # 4. Submit Step 3 (Threat Event) [Formerly Step 2]
        response = self.app.post('/assessment/step/3', data={'threat_event': 'SQL Injection'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Step 4', response.data)

        # Fast forward through steps 4-11
        for i in range(4, 12):
            data = {}
            if i == 8: data = {'likelihood_initiation': '3'} # Step 7 -> 8
            if i == 9: data = {'likelihood_impact': '4'}     # Step 8 -> 9
            if i == 11: data = {'impact_level': '5', 'financial_impact': '50000'} # Step 10 -> 11
            
            response = self.app.post(f'/assessment/step/{i}', data=data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

        # After step 11, should be at result
        self.assertIn(b'Risk Assessment Result', response.data)
        
        # Verify Risk Calculation Display
        self.assertIn(b'Very High', response.data)
        self.assertIn(b'Customer DB', response.data) # Verify Asset Name
        self.assertIn(b'50000', response.data)       # Verify Financial Impact

if __name__ == '__main__':
    unittest.main()
