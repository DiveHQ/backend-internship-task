from django.urls import path
from knox import views as knox_views
from .views import RegisterAPI,LoginAPI
from .views import CaloView
urlpatterns = [
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path('register',RegisterAPI.as_view()),
    path("project",CaloView.as_view()),
    path("project/<int:id>",CaloView.as_view())

]