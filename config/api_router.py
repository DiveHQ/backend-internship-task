from django.urls.conf import include, path

app_name = "api"
urlpatterns = [path("", include("api_project.users.urls"))]
