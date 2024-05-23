import unittest
from models import users, loans, repayments
from app import app

class LoanAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        users.clear()
        loans.clear()
        repayments.clear()

    def test_user_registration(self):
        response = self.app.post('/register', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 201)

    def test_user_login(self):
        self.app.post('/register', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        response = self.app.post('/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)

    def test_loan_creation(self):
        self.app.post('/register', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        login_response = self.app.post('/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        access_token = login_response.get_json()['access_token']
        response = self.app.post('/loan', json={
            'amount': 10000,
            'term': 3
        }, headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 201)

    def test_loan_approval(self):
        self.app.post('/register', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        login_response = self.app.post('/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        access_token = login_response.get_json()['access_token']
        self.app.post('/loan', json={
            'amount': 10000,
            'term': 3
        }, headers={'Authorization': f'Bearer {access_token}'})
        response = self.app.post('/loan/1/approve', headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 200)

    def test_repayment(self):
        self.app.post('/register', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        login_response = self.app.post('/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        access_token = login_response.get_json()['access_token']
        self.app.post('/loan', json={
            'amount': 10000,
            'term': 3
        }, headers={'Authorization': f'Bearer {access_token}'})
        response = self.app.post('/repayment', json={
            'repayment_id': 1,
            'amount': 3333.33
        }, headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
