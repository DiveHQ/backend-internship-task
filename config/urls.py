from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# from django.contrib.auth.decorators import login_required

schema_view = get_schema_view(
    openapi.Info(
        title="API Project",
        default_version="v1",
        description="API Project description",
        terms_of_service="",
        contact=openapi.Contact(email="engineering@api-project.com"),
        license=openapi.License(name="Copyright"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


# Authentication views for redoc and swagger
# To Use: Replace corresponding view with these login_required views
# Use django.contrib.auth.views.decorators.login_required() to add login to a view
# U can also use django.contrib.admin.views.decorators.staff_member_required()
# Redoc
@staff_member_required(login_url="/login/")
def redoc(request):
    return schema_view.with_ui("redoc", cache_timeout=0)(request)


# Swagger
@staff_member_required(login_url="/login/")
def swagger(request):
    return schema_view.with_ui("swagger", cache_timeout=0)(request)


urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    # path(
    #     "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    # ),
    # A path for login_required to use for authentication. Relies on Django auth system
    path("login/", auth_views.LoginView.as_view(), name="login"),
    # API Docs
    # path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # path(
    #     "swagger-docs/",
    #     schema_view.with_ui("swagger", cache_timeout=0),
    #     name="schema-swagger-ui",
    # ),
    # Protected API Docs
    path("docs/", redoc, name="schema-redoc"),
    path("swagger-docs/", swagger, name="schema-swagger-ui"),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
