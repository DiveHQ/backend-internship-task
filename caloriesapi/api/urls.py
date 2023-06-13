from django.urls import path
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Calorie Entry Rest API",
        default_version="v1",
        description="Write a REST API for the input of calories in Python",
        terms_of_service="",
        contact=openapi.Contact(email="ralphvwilliams@icloud.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("account/create/", views.create_account),
    path("login/", views.user_login),
    path("logout/", views.user_logout),
    path("entry/", views.create_calorie_entry),
    path("entry/<int:pk>", views.get_calorie_entry),
    path("entry/update/<int:pk>", views.update_calorie_entry),
    path("entry/delete/<int:pk>", views.delete_calorie_entry),
    path("entries/", views.get_calorie_entries),
    path("entries/date", views.get_calorie_entries_by_date),
    path("entries/status", views.get_calorie_entries_by_status),
    path("users/", views.get_users),
    path("user/<int:user_id>", views.update_user_groups),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "docs/redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
