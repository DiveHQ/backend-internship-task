from django.contrib import admin
from .models import Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Entry model.

    This admin configuration provides a customized interface for managing Entry instances in the Django admin site.

    Attributes:
        list_display (tuple/list): The fields to display in the entry list view.
        list_filter (tuple/list): The fields to use for filtering the entry list.
        search_fields (tuple/list): The fields to use for searching entries.
        date_hierarchy (str): The field to use for hierarchical date-based navigation.

    """

    list_display = ('user', 'date', 'time', 'text', 'calories', 'meets_calorie_expectation')
    list_filter = ('user', 'date', 'meets_calorie_expectation')
    search_fields = ('text',)
    date_hierarchy = 'date'
