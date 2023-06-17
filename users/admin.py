from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import User


admin.site.site_header = "DiveHQ Admin"
admin.site.site_title = "DiveHQ Admin Portal"
admin.site.index_title = "Welcome to DiveHQ Portal"



@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """
    Admin configuration for the User model.
    """

    list_display = ('email', 'full_name', 'is_staff', 'is_admin', 'is_user_manager')
    list_filter = ('is_staff', 'is_admin', 'is_user_manager')
    search_fields = ('email', 'full_name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('full_name', 'phone_number', 'expected_calories')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_admin', 'is_user_manager')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    def get_inline_instances(self, request, obj=None):
        """
        Hide the default inline user profile model.
        """
        return []

    def has_delete_permission(self, request, obj=None):
        """
        Prevent superusers from being deleted via the admin.
        """
        return obj is None or not obj.is_superuser
