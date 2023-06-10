from rest_framework.routers import SimpleRouter

from .views import CaloriesView

router = SimpleRouter()

router.register("", CaloriesView, "calories")


urlpatterns = router.urls
