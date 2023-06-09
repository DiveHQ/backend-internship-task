import pytest

from api_project.common.utils import BulkCreateManager
from api_project.users.models import User

pytestmark = pytest.mark.django_db


class TestBulkCreateManager:
    def test_efficient_bulk_creation(self):
        manager = BulkCreateManager(chunk_size=2)
        for index in range(10):
            manager.add(User(name=f"Test User {index}", email=f"email{index}@test.com"))
        assert User.objects.count() == 10
        manager.done()
        assert User.objects.count() == 10

    def test_final_partial_chunk_is_saved(self):
        manager = BulkCreateManager(chunk_size=3)
        for index in range(10):
            manager.add(User(name=f"Test User {index}", email=f"email{index}@test.com"))
        assert User.objects.count() == 9
        manager.done()
        assert User.objects.count() == 10
