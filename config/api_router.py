from django.urls.conf import include, path

# from rest_framework.routers import SimpleRouter

# from api_project.users import views as user_views


# user_router = SimpleRouter()
# user_router.register("", user_views.UserViewSet, basename="users")


app_name = "api"
urlpatterns = [
    # path("users/", include(user_router.urls)),
    path("", include("api_project.users.urls"))
]
