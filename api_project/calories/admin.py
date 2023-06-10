from django.contrib import admin

from .models import Calories


@admin.register(Calories)
class CaloriesAdmin(admin.ModelAdmin):
    list_display = ("__str__", "meal")
    search_fields = ("id", "user__id")
