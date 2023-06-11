from django.contrib.auth import get_user_model

User = get_user_model()

USER_MANAGER_GROUP = "User Managers"

COMMON_FILTERS = {
    "contains_exact": ["contains", "startswith", "endswith", "exact", "iexact"],
    "gt_lt": ["gt", "lt", "gte", "lte"],
}
