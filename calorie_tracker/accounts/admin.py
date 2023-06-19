from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "expected_calories",
        "role",
    ) 
    list_filter = ("role",)  


# Register your models here.
admin.site.register(User, CustomUserAdmin)
