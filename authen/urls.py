from django.urls import path
from knox import views as knox_views
from .views import RegisterAPI,LoginAPI,UserManger

urlpatterns = [
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),

    path('register',RegisterAPI.as_view()),
    path("api/v1/manager/<int:id>", UserManger.as_view() ),
    path("api/v1/manager/", UserManger.as_view())

]