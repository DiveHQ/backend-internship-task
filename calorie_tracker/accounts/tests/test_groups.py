import pytest
from accounts.constants import ADMIN_GROUP, USER_MANAGER_GROUP
from django.contrib.auth.models import Group


@pytest.mark.django_db
def test_groups_are_persisted():
    """Test that groups are persisted after migrations."""
    groups = [USER_MANAGER_GROUP, ADMIN_GROUP]

    for group in groups:
        assert Group.objects.filter(name=group).exists()
