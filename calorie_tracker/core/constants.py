from django.contrib.auth import get_user_model

User = get_user_model()

COMMON_FILTER_LOOKUPS = {
    "contains_exact": ["contains", "startswith", "endswith", "exact", "iexact"],
    "gt_lt": ["gt", "lt", "gte", "lte"],
}
