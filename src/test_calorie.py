import unittest
from unittest.mock import patch
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.database import User, Calories
from src.app import calorie

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calorie.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)
app.register_blueprint(calorie)

class CalorieTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calories.db'
        self.app.register_blueprint(calorie)
        self.client = self.app.test_client()
        self.db = SQLAlchemy(self.app)
        self.db.create_all()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    def test_get_authenticated_user_role(self):
        with self.app.test_request_context():
            # Create a test user
            user = User(username='test_user', role='regular')
            self.db.session.add(user)
            self.db.session.commit()

            # Set the current user for the request context
            with patch('flask_jwt_extended.get_jwt_identity') as mock_get_jwt_identity:
                mock_get_jwt_identity.return_value = user.id
                response = self.client.get('/api/v1/calorie', headers={'Authorization': 'Bearer test_token'})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json['message'], 'regular')

    def test_get_authenticated_user(self):
        with self.app.test_request_context():
            # Create a test user
            user = User(username='test_user', expected_calories=2000)
            self.db.session.add(user)
            self.db.session.commit()

            # Set the current user for the request context
            with patch('flask_jwt_extended.get_jwt_identity') as mock_get_jwt_identity:
                mock_get_jwt_identity.return_value = user.id
                response = self.client.get('/api/v1/calorie', headers={'Authorization': 'Bearer test_token'})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json['username'], 'test_user')
                self.assertEqual(response.json['expected_calories'], 2000)

    def test_is_valid_user(self):
        with self.app.test_request_context():
            # Create a test user
            user = User(username='test_user')
            self.db.session.add(user)
            self.db.session.commit()

            self.assertTrue(user.test_is_valid_user('test_user'))
            self.assertFalse(user.test_is_valid_user('non_existing_user'))

    @patch('app.fetch_calories_from_api')
    def test_create_meal(self, mock_fetch_calories_from_api):
        with self.app.test_request_context():
            # Create a test user
            user = User(username='test_user', expected_calories=2000)
            self.db.session.add(user)
            self.db.session.commit()

            # Mock the API response for fetch_calories_from_api
            mock_fetch_calories_from_api.return_value = 300

            # Set the current user for the request context
            with patch('flask_jwt_extended.get_jwt_identity') as mock_get_jwt_identity:
                mock_get_jwt_identity.return_value = user.id
                response = self.client.post('/api/v1/calorie',
                                            json={'date': '2022-01-01', 'time': '12:00', 'text': 'test_meal'},
                                            headers={'Authorization': 'Bearer test_token'})

                self.assertEqual(response.status_code, 201)
                self.assertEqual(response.json['message'], 'Meal created successfully')
                self.assertEqual(response.json['meal']['date'], '2022-01-01')
                self.assertEqual(response.json['meal']['time'], '12:00')
                self.assertEqual(response.json['meal']['meal'], 'test_meal')
                self.assertEqual(response.json['meal']['calorie'], 300)
                self.assertFalse(response.json['meal']['is_below_expected'])

    def test_get_meal(self):
        with self.app.test_request_context():
            # Create a test user
            user = User(username='test_user', expected_calories=2000)
            self.db.session.add(user)

            # Create a test meal
            meal = Calories(date='2022-01-01', time='12:00', meal='test_meal', calorie=300, user_id='test_user')
            self.db.session.add(meal)

            self.db.session.commit()

            response = self.client.get('/api/v1/calorie/1')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['meal']['date'], '2022-01-01')
            self.assertEqual(response.json['meal']['time'], '12:00')
            self.assertEqual(response.json['meal']['meal'], 'test_meal')
            self.assertEqual(response.json['meal']['calorie'], 300)

    def test_update_meal(self):
        with self.app.test_request_context():
            # Create a test user
            user = User(username='test_user', expected_calories=2000)
            self.db.session.add(user)

            # Create a test meal
            meal = Calories(date='2022-01-01', time='12:00', meal='test_meal', calorie=300, user_id='test_user')
            self.db.session.add(meal)

            self.db.session.commit()

            response = self.client.put('/api/v1/calorie/1',
                                        json={'date': '2022-01-02', 'time': '13:00', 'text': 'updated_meal', 'calories': 400})

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['message'], 'Meal updated successfully')
            self.assertEqual(response.json['meal']['date'], '2022-01-02')
            self.assertEqual(response.json['meal']['time'], '13:00')
            self.assertEqual(response.json['meal']['meal'], 'updated_meal')
            self.assertEqual(response.json['meal']['calorie'], 400)
            self.assertFalse(response.json['meal']['is_below_expected'])

    def test_delete_meal(self):
        with self.app.test_request_context():
            # Create a test user
            user = User(username='test_user', expected_calories=2000)
            self.db.session.add(user)

            # Create a test meal
            meal = Calories(date='2022-01-01', time='12:00', meal='test_meal', calorie=300, user_id='test_user')
            self.db.session.add(meal)

            self.db.session.commit()

            response = self.client.delete('/api/v1/calorie/1')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['message'], 'Meal deleted successfully')

if __name__ == '__main__':
    unittest.main()
