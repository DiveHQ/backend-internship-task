from factory.django import DjangoModelFactory

from api_project.calories.models import Calories


class CaloriesFactory(DjangoModelFactory):
    class Meta:
        model = Calories
