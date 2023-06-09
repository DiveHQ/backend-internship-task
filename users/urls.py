from django.urls import path 
from .views import RegistrationView, UserDetailsView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegistrationView.as_view(), name='register_user'),
    path('details/<int:pk>/', UserDetailsView.as_view(), name='edit_user_details')
]