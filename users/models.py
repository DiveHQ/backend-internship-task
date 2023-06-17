from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """
    Custom user manager for the User model.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create a regular user.

        Args:
            email (str): Email address of the user.
            password (str, optional): User's password. Defaults to None.
            **extra_fields: Additional fields for the user.

        Returns:
            User: Created user instance.

        Raises:
            ValueError: If email is not provided.
        """

        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create a superuser.

        Args:
            email (str): Email address of the superuser.
            password (str, optional): Superuser's password. Defaults to None.
            **extra_fields: Additional fields for the superuser.

        Returns:
            User: Created superuser instance.

        Raises:
            ValueError: If email is not provided.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    """
    username = None
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, null=True)
    expected_calories = models.IntegerField(null=True)
    is_admin = models.BooleanField(default=False)
    is_user_manager = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    def __str__(self):
        return self.email


