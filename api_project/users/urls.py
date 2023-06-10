from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import SignUpView, UserView

router = DefaultRouter()

router.register("users", UserView, basename="users")


urlpatterns = [
    path("auth/signup/", SignUpView.as_view(), name="signup"),
    path("auth/login/", TokenObtainPairView.as_view(), name="token-obtain"),
    path("auth/refresh-token/", TokenRefreshView.as_view(), name="token-refresh"),
    path("", include(router.urls)),
]
