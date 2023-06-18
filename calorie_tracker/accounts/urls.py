from django.urls import path
from accounts.views import UserRegistrationView, UserLoginView, UserLogoutView

urlpatterns = [
    # Other URL patterns
    path("api/register/", UserRegistrationView.as_view(), name="user_registration"),
    path("api/login/", UserLoginView.as_view(), name="user_login"),
    path("api/logout/", UserLogoutView.as_view(), name="user_logout"),
]
