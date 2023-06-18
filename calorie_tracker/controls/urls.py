from django.urls import path
from .views import *

urlpatterns = [
    path("profile", profile, name="profile"),
    path("tracker/entries/all/", all_entries, name="all_entries"),
    path("users/all/", all_users, name="all_users"),
]
