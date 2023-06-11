from django_filters.rest_framework import FilterSet

from .constants import User


class UserFilter(FilterSet):
    """Filter class for the User model."""

    class Meta:
        model = User
        fields = {
            "username": ["contains"],
            "first_name": ["contains"],
            "last_name": ["contains"],
            "email": ["contains"],
            "is_staff": ["exact"],
            "is_active": ["exact"],
            "is_superuser": ["exact"],
            "date_joined": ["gt", "lt"],
        }
