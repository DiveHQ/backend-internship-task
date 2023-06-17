from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('delete/', views.DeleteUserView.as_view(), name='delete'),
    path('update/', views.UpdateUserView.as_view(), name='update'),
    path('list/', views.ListUsersView.as_view(), name='list_users'),
    path('detail/', views.UserDetailView.as_view(), name='get_user'),
]
