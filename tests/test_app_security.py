import unittest
import os
from app import app

class TestAppSecurity(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_security_headers(self):
        """Test that security headers are present in the response."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        
        # Check HSTS
        self.assertIn('Strict-Transport-Security', response.headers)
        self.assertEqual(response.headers['Strict-Transport-Security'], 'max-age=31536000; includeSubDomains')
        
        # Check X-Content-Type-Options
        self.assertIn('X-Content-Type-Options', response.headers)
        self.assertEqual(response.headers['X-Content-Type-Options'], 'nosniff')
        
        # Check X-Frame-Options
        self.assertIn('X-Frame-Options', response.headers)
        self.assertEqual(response.headers['X-Frame-Options'], 'SAMEORIGIN')

    def test_dev_config_defaults(self):
        """Test that development config is used by default (when FLASK_ENV is not production)."""
        # Ensure we are not in production mode for this test
        if 'FLASK_ENV' in os.environ:
            del os.environ['FLASK_ENV']
            
        # Reload app config if necessary (though app is already imported)
        # In a real scenario, we might need to reload the module or create a factory
        # For this simple app, we check the current state which should be dev defaults
        
        self.assertFalse(app.config['SESSION_COOKIE_SECURE'])
        self.assertEqual(app.config['SECRET_KEY'], 'dev-secret-key-change-in-prod')

if __name__ == '__main__':
    unittest.main()
