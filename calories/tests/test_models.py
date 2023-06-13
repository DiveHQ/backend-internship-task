from django.test import TestCase
from rest_framework.authtoken.models import Token
from users.models import User
from calory_limit.models import CaloryLimit
from ..models import Calories

class CaloryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            role='Regular'
        )
        self.user.set_password('testpassword')
        self.user.save()
        

        self.calory_limit = CaloryLimit.objects.create(
            calory_limit = 55,
            description = 'I am burning these',
            user = self.user
        )

    def test_calory_creation(self):
        calory = Calories.objects.create(
            text = 'Apple',
            calories = 44,
            user = self.user,
            calory_limit = self.calory_limit
        )

        self.assertIsInstance(calory, Calories)
        self.assertEqual(calory.text, 'Apple')
        self.assertEqual(calory.__str__(), 'Apple')

