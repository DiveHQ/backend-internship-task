from django.contrib import admin
from .models import Entry

# Register your models here.


class CustomEntryModel(admin.ModelAdmin):
    list_display = ("user", "text", "calories", "date")
    list_filter = ["user__role"]


admin.site.register(Entry, CustomEntryModel)
