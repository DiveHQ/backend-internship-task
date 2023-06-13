"""URL conf for accounts app."""
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserSettingViewSet, UserViewSet

app_name = "accounts"

router = DefaultRouter()
router.register("users", UserViewSet)
router.register("user-settings", UserSettingViewSet)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
] + router.urls
