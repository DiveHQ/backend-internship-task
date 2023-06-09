from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _

from api_project.common import models as base_models


class UserManager(base_models.BaseManager, BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a user with given email and password
        """
        if not email:
            raise ValueError(_("The email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(PermissionsMixin, base_models.BaseModel, AbstractBaseUser):
    """Default user for api_project."""

    class Roles(models.TextChoices):
        MANAGER = "manager", _("Manager")
        ADMIN = "admin", _("Admin")
        USER = "user", _("User")

    email = models.EmailField(unique=True, max_length=255, blank=False, null=False)
    #: First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into the admin site"),
    )
    role = models.CharField(max_length=25, choices=Roles.choices, default=Roles.USER)
    deleted = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self) -> str:
        return self.get_full_name() or self.email
