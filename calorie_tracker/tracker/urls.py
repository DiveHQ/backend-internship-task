from django.urls import path
from .views import *

urlpatterns = [
    path("profile", profile, name="profile"),
    path("entries/", entry_list, name="entry_list"),
    path("entries/<int:pk>/", entry_detail, name="entry_detail"),
    path("entries/all/", all_entries, name="all_entries"),
    path("users/all/", all_users, name="all_users"),
]
