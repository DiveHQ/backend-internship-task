from django.test import TestCase
from users.models import User
from ..models import CaloryLimit

class CaloryLimitModelTest(TestCase):
    def setUp(self):
        # Create a user for the test
        self.user = User.objects.create(email='testuser@gmail.com')

    def test_calory_limit_creation(self):
        # Create a CaloryLimit object
        calory_limit = CaloryLimit.objects.create(
            calory_limit=2000,
            description='Sample description',
            user=self.user,
            exceeded_maximum=False,
            present_calory_amount=1500
        )

        # Assert that the object is created successfully
        self.assertIsInstance(calory_limit, CaloryLimit)
        self.assertEqual(calory_limit.calory_limit, 2000)
        self.assertEqual(calory_limit.description, 'Sample description')
        self.assertEqual(calory_limit.user, self.user)
        self.assertFalse(calory_limit.exceeded_maximum)
        self.assertEqual(calory_limit.present_calory_amount, 1500)
