from django.urls import path

from . import views

urlpatterns = [
    # users
    path("login/", views.Login.as_view(), name="token_obtain_pair"),
    path("register/", views.Register.as_view(), name="register"),
    # access profile
    path("profile/", views.UserProfile.as_view()),
    # refresh and verify token
    path("refresh/", views.RefreshToken.as_view(), name="token_refresh"),
]
