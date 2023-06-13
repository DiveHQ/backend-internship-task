"""URL conf for the tracker app."""
from rest_framework.routers import DefaultRouter

from .views import EntryViewSet

app_name = "tracker"

router = DefaultRouter()
router.register("entries", EntryViewSet)

urlpatterns = router.urls
