from django_filters.rest_framework import FilterSet

from backend.constants import COMMON_FILTER_LOOKUPS as _

from .models import Entry


class EntryFilter(FilterSet):
    """Filter class for the Entry model."""

    class Meta:
        model = Entry
        fields = {
            "user": ["exact"],
            "text": _["contains_exact"],
            "date": _["gt_lt"],
            "time": _["gt_lt"],
            "calories": _["gt_lt"],
            "below_daily_threshold": ["exact"],
        }
