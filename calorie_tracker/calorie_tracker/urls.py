"""calorie_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import include, path
from rest_framework import routers
from tracker.views import register_user,login_user
from tracker.views import create_entry, get_entries, update_entry, delete_entry,check_calorie_goal
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', get_entries, name='entry-list'),
    path('entries/create/', create_entry, name='entry-create'),
    path('entries/update/<int:pk>/', update_entry, name='entry-update'),
    path('entries/delete/<int:pk>/', delete_entry, name='entry-delete'),
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
    path('check-calorie-goal/<str:date>/', check_calorie_goal, name='check_calorie_goal'),
]
