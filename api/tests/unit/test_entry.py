# app/tests/unit/test_entry.py

import pytest
from api.models.entry import Entry

def test_entry_model():
    entry = Entry(user_id=1, text='Example Text', is_satisfied=True, calories=500)
    assert entry.user_id == 1
    assert entry.text == 'Example Text'
    assert entry.is_satisfied == True
    assert entry.calories == 500
