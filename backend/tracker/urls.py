from rest_framework.routers import DefaultRouter

from . import views

app_name = "tracker"

router = DefaultRouter()
router.register("", views.EntryViewSet)

urlpatterns = router.urls
