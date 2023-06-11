from django_filters import CharFilter
from django_filters.rest_framework import FilterSet

from .constants import COMMON_FILTERS as f
from .constants import User


class UserFilter(FilterSet):
    """Filter class for the User model."""

    username = CharFilter()

    class Meta:
        model = User
        fields = {
            "username": f["contains_exact"],
            "first_name": f["contains_exact"],
            "last_name": f["contains_exact"],
            "email": f["contains_exact"],
            "is_staff": ["exact"],
            "is_active": ["exact"],
            "is_superuser": ["exact"],
            "date_joined": f["gt_lt"],
        }
