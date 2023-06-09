from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import CustomDjoserViewSet

app_name = "users"

if settings.DEBUG:
    user_router = DefaultRouter()
else:
    user_router = SimpleRouter()

user_router.register("", CustomDjoserViewSet, basename="users")


urlpatterns = [
    path("auth/", include(user_router.urls)),
    path("auth/", include("djoser.urls.jwt")),
]
