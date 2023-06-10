from django.urls.conf import include, path

app_name = "api"

urlpatterns = [
    path("calories/", include("api_project.calories.urls")),
    path("", include("api_project.users.urls")),
]
