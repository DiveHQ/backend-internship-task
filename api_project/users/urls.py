from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import SignUpView, UserView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserView, basename="users")


urlpatterns = [
    path("auth/signup/", SignUpView.as_view(), name="signup"),
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain"),
    path("auth/refresh-token/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]
