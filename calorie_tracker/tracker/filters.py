from core.constants import COMMON_FILTER_LOOKUPS as _
from django_filters import CharFilter
from django_filters.rest_framework import FilterSet

from .models import Entry


class EntryFilter(FilterSet):
    """Filter class for the Entry model."""

    username = CharFilter()

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
