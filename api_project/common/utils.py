from collections import defaultdict

from django.apps import apps
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode
from django_filters.filters import BaseInFilter, CharFilter
from rest_framework.filters import OrderingFilter


def encode_uid(pk):
    return force_str(urlsafe_base64_encode(force_bytes(pk)))


class CustomOrderingFilter(OrderingFilter):
    """Custom OrderingFilter with fields for description"""

    def get_schema_fields(self, view):
        check = hasattr(view, "ordering_fields")

        if check:
            fields = [f"`{field}`" for field in view.ordering_fields]
            reverse_fields = [f"`-{field}`" for field in view.ordering_fields]

            self.ordering_description = (
                f"Fields to use when ordering the results: {', '.join(fields)}. "
                f"The client may also specify reverse orderings by prefixing the field name "
                f"with `-`: {', '.join(reverse_fields)}."
            )

        return super().get_schema_fields(view)


class CharInFilter(BaseInFilter, CharFilter):
    """Allow filtering on comma separated characters

    Example usage:

    # models.py
    class Gender(models.Model):
        name = models.CharField(
            _("Name"), max_length=50, blank=True
        )

        class Meta:
            ordering = ["name"]

        def __str__(self):
            return str(self.name)

    class Profile(models.Model):
        genders = models.ManyToManyField(Gender, verbose_name=_("Gender"), blank=True,)


    # filters.py
    gender = CharInFilter(
        field_name="genders__name",
        lookup_expr="in",
        help_text=(
            "Filter by gender name"
            "Values can be comma separated. Eg. `gender=Male,Female`"
        ),
    )
    """

    pass


class BulkCreateManager(object):
    """
    This helper class keeps track of ORM objects to be created for multiple
    model classes, and automatically creates those objects with `bulk_create`
    when the number of objects accumulated for a given model class exceeds
    `chunk_size`.
    Upon completion of the loop that's `add()`ing objects, the developer must
    call `done()` to ensure the final set of objects is created for all models.
    """

    def __init__(self, chunk_size=100):
        self._create_queues = defaultdict(list)
        self.chunk_size = chunk_size

    def _commit(self, model_class):
        model_key = model_class._meta.label
        model_class.objects.bulk_create(
            self._create_queues[model_key], ignore_conflicts=True
        )
        self._create_queues[model_key] = []

    def add(self, obj):
        """
        Add an object to the queue to be created, and call bulk_create if we
        have enough objs.
        """
        model_class = type(obj)
        model_key = model_class._meta.label
        self._create_queues[model_key].append(obj)
        if len(self._create_queues[model_key]) >= self.chunk_size:
            self._commit(model_class)

    def done(self):
        """
        Always call this upon completion to make sure the final partial chunk
        is saved.
        """
        for model_name, objs in self._create_queues.items():
            if len(objs) > 0:
                self._commit(apps.get_model(model_name))
