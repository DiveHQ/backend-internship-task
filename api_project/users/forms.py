from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = "__all__"
        exclude = [
            "password",
        ]

        error_messages = {"email": {"unique": _("This email has already been taken.")}}
