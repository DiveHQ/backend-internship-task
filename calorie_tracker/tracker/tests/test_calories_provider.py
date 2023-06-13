import pytest
from tracker.helpers import retrieve_calories


@pytest.mark.skip
def test_calories_provider_is_up():
    """Test that calories provider is up."""
    calories = retrieve_calories(query="1 bowl of rice.")
    calories_in_a_bowl_of_rice = 410.8

    assert calories == calories_in_a_bowl_of_rice
