from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Entry
class EntryTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        # Create entries for the user
        self.entry1 = Entry.objects.create(
            user=self.user,
            date='2023-06-16',
            meal='Breakfast',
            calories=300
        )
        self.entry2 = Entry.objects.create(
            user=self.user,
            date='2023-06-16',
            meal='Lunch',
            calories=500
        )

    def test_calculate_total_calories(self):
        # Calculate the total calories for the user on a specific date
        date = '2023-06-16'
        total_calories = Entry.objects.filter(user=self.user, date=date).aggregate(total=Sum('calories'))['total']
        
        # Assert that the calculated total calories match the expected value
        self.assertEqual(total_calories, 800)

    def test_check_calorie_goal(self):
        # Set the calorie goal for the user
        self.user.calorie_goal = 1000
        self.user.save()

        # Check if the calorie goal is met for a specific date
        date = '2023-06-16'
        entries = Entry.objects.filter(user=self.user, date=date)
        total_calories = entries.aggregate(total=Sum('calories'))['total']
        is_goal_met = total_calories < self.user.calorie_goal

        # Assert that the calorie goal status matches the expected value
        self.assertTrue(is_goal_met)
