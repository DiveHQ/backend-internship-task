import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)


class BaseManager(models.Manager):
    def get_queryset(self):
        return BaseQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def inactive(self):
        return self.get_queryset().inactive()


class BaseModel(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created_at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))
    is_active = models.BooleanField(default=True)

    objects = BaseManager()

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return str(self.pk)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.pk}>"

    def activate(self):
        if not self.is_active:
            self.is_active = True
            self.save(update_fields=["is_active", "updated_at"] if self.pk else None)

    def deactivate(self):
        if self.is_active:
            self.is_active = False
            self.save(update_fields=["is_active", "updated_at"] if self.pk else None)
