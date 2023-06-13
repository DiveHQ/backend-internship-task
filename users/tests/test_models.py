from django.db import models
from django.test import TestCase
from ..models import User
from django.db.utils import IntegrityError

class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            role='Regular'
        )
        user.set_password('testpassword')
        user.save()

        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.role, 'Regular')

        # Test password hashing
        self.assertTrue(user.check_password('testpassword'))

    def test_user_uniqueness(self):
        User.objects.create(
            email='existing@example.com',
            first_name='Existing',
            last_name='User',
            role='Regular'
        )

        # Attempt to create a user with the same email
        with self.assertRaises(IntegrityError):
            User.objects.create(
                email='existing@example.com',
                first_name='Duplicate',
                last_name='User',
                role='Regular'
            )

