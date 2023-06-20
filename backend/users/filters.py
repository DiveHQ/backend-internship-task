from django_filters.rest_framework import FilterSet

from backend.constants import COMMON_FILTER_LOOKUPS as _

from .models import User


class UserFilter(FilterSet):
    """Filter class for the User model."""

    class Meta:
        model = User
        fields = {
            "username": _["contains_exact"],
            "first_name": _["contains_exact"],
            "last_name": _["contains_exact"],
            "email": _["contains_exact"],
            "is_staff": ["exact"],
            "is_active": ["exact"],
            "is_superuser": ["exact"],
            "date_joined": _["gt_lt"],
        }
