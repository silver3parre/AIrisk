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
        # 1. Start Assessment
        response = self.app.get('/assessment/start', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Step 1', response.data)

        # 2. Submit Step 1 (Threat Source)
        response = self.app.post('/assessment/step/1', data={'threat_source': 'External Hacker'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Step 2', response.data)

        # 3. Submit Step 2 (Threat Event)
        response = self.app.post('/assessment/step/2', data={'threat_event': 'SQL Injection'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Step 3', response.data)

        # Simulate skipping to result (assuming we fill necessary data in session or steps are optional/handled)
        # For this test, let's just jump to result if logic allows, or fill minimums.
        # The app logic checks step > 10 to go to result.
        
        # Let's fast forward through steps 3-10 with dummy data
        for i in range(3, 11):
            data = {}
            if i == 7: data = {'likelihood_initiation': '3'}
            if i == 8: data = {'likelihood_impact': '4'}
            if i == 10: data = {'impact_level': '5'}
            
            response = self.app.post(f'/assessment/step/{i}', data=data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

        # After step 10, should be at result
        self.assertIn(b'Risk Assessment Result', response.data)
        
        # Verify Risk Calculation Display
        # 3 (Mod) x 4 (High) -> Overall Likelihood 4 (High)
        # Likelihood 4 (High) x Impact 5 (Very High) -> Risk 5 (Very High)
        self.assertIn(b'Very High', response.data)

if __name__ == '__main__':
    unittest.main()
