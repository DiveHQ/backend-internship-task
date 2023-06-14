from django.urls import path
from knox import views as knox_views
from .views import RegisterAPI,LoginAPI
urlpatterns = [
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('register',RegisterAPI.as_view()),
]
