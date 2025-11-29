import unittest
from app import app, db
from models import Assessment
import os

class RBACScopingTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self, username, role):
        return self.client.post('/login', data=dict(
            username=username,
            role=role
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('testuser', 'Analyst')
        self.assertIn(b'Welcome, testuser!', rv.data)
        rv = self.logout()
        self.assertIn(b'You have been logged out.', rv.data)

    def test_viewer_access_control(self):
        self.login('viewer', 'Viewer')
        # Viewer should not access start assessment
        rv = self.client.get('/assessment/start', follow_redirects=True)
        self.assertIn(b'You do not have permission', rv.data)
        
    def test_analyst_scoping_flow(self):
        self.login('analyst', 'Analyst')
        
        # 1. Start Assessment -> Redirects to Scope
        rv = self.client.get('/assessment/start', follow_redirects=True)
        self.assertIn(b'Pre-Assessment Scoping', rv.data)
        
        # 2. Submit Scope
        rv = self.client.post('/assessment/scope', data=dict(
            assessment_title='Test Assessment',
            security_categorization='High',
            system_description='Test System'
        ), follow_redirects=True)
        
        # Should redirect to Step 1
        self.assertIn(b'Step 1: Identify Asset', rv.data)
        
        # 3. Verify Session Data (via saving)
        # Fast forward to save (skipping steps for test speed, assuming session holds scope)
        # We need to populate minimal data to save
import unittest
from app import app, db
from models import Assessment
import os

class RBACScopingTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self, username, role):
        return self.client.post('/login', data=dict(
            username=username,
            role=role
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('testuser', 'Analyst')
        self.assertIn(b'Welcome, testuser!', rv.data)
        rv = self.logout()
        self.assertIn(b'You have been logged out.', rv.data)

    def test_viewer_access_control(self):
        self.login('viewer', 'Viewer')
        # Viewer should not access start assessment
        rv = self.client.get('/assessment/start', follow_redirects=True)
        self.assertIn(b'You do not have permission', rv.data)
        
    def test_analyst_scoping_flow(self):
        self.login('analyst', 'Analyst')
        
        # 1. Start Assessment -> Redirects to Scope
        rv = self.client.get('/assessment/start', follow_redirects=True)
        self.assertIn(b'Pre-Assessment Scoping', rv.data)
        
        # 2. Submit Scope
        rv = self.client.post('/assessment/scope', data=dict(
            assessment_title='Test Assessment',
            security_categorization='High',
            system_description='Test System'
        ), follow_redirects=True)
        
        # Should redirect to Step 1
        self.assertIn(b'Step 1: Identify Asset', rv.data)
        
        # 3. Verify Session Data (via saving)
        # Fast forward to save (skipping steps for test speed, assuming session holds scope)
        # We need to populate minimal data to save
        with self.client.session_transaction() as sess:
            sess['assessment_data']['asset_name'] = 'Test Asset'
            sess['assessment_data']['asset_type'] = 'Data'
            # Add other required fields if validation is strict, but save_assessment is lenient
        
        rv = self.client.post('/assessment/save', follow_redirects=True)
        # 4. Verify Dashboard
        rv = self.client.get('/dashboard')
        self.assertIn(b'Test Assessment', rv.data)
        self.assertIn(b'High', rv.data)
        self.assertIn(b'analyst', rv.data)

    def test_admin_delete_assessment(self):
        # 1. Create Assessment as Analyst
        self.client.post('/login', data=dict(username='analyst', role='Analyst'), follow_redirects=True)
        self.client.post('/assessment/scope', data=dict(
            assessment_title='To Be Deleted',
            security_categorization='Low',
            system_description='Desc'
        ), follow_redirects=True)
        
        # Save it
        with self.client.session_transaction() as sess:
            sess['assessment_data']['asset_name'] = 'Asset 1'
            
        self.client.post('/assessment/save', follow_redirects=True)
        
        # Get ID (it should be 1 since it's a fresh DB)
        
        # 2. Login as Admin
        self.client.get('/logout', follow_redirects=True)
        self.client.post('/login', data=dict(username='admin', role='Admin'), follow_redirects=True)
        
        # 3. Delete
        rv = self.client.post('/assessment/delete/1', follow_redirects=True)
        self.assertIn(b'Assessment deleted successfully', rv.data)
        self.assertNotIn(b'To Be Deleted', rv.data)

    def test_analyst_cannot_delete(self):
        # 1. Create Assessment
        self.client.post('/login', data=dict(username='analyst', role='Analyst'), follow_redirects=True)
        self.client.post('/assessment/scope', data=dict(
            assessment_title='Analyst Assessment',
            security_categorization='Low',
            system_description='Desc'
        ), follow_redirects=True)
        self.client.post('/assessment/save', follow_redirects=True)
        
        # 2. Attempt Delete
        rv = self.client.post('/assessment/delete/1', follow_redirects=True)
        # Should be forbidden or redirect to index with flash
        self.assertIn(b'You do not have permission', rv.data)
        # Assessment should still exist
        rv = self.client.get('/dashboard')
        self.assertIn(b'Analyst Assessment', rv.data)

if __name__ == '__main__':
    unittest.main()
