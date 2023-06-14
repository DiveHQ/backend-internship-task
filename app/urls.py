from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
   openapi.Info(
      title="DiveHQ Backend Development",
      default_version='v1',
      description="Test API's of Calory Tracker App",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="gibrilissakaiddrisu@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/calories/', include('calories.urls')),
    path('api/calories/limit/', include('calory_limit.urls'))
]
