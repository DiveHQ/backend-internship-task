# app/tests/unit/test_user.py

import pytest
from api.models.user import User

def test_user_model():
    user = User(username='example_user', password='password', role='regular', calorie_perday=2000)
    assert user.username == 'example_user'
    assert user.password == 'password'
    assert user.role == 'regular'
    assert user.calorie_perday == 2000
