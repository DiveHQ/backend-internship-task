import pytest


@pytest.fixture
def entry_payload():
    """Return sample entry information as a payload."""
    return {
        "text": "A loaf of bread.",
        "calories": 500,
    }
