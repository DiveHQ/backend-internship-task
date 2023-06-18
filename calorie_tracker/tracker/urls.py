from django.urls import path
from .views import entry_list, entry_detail, all_entries

urlpatterns = [
    path("entries/", entry_list, name="entry_list"),
    path("entries/<int:pk>/", entry_detail, name="entry_detail"),
    path("all-records/", all_entries, name="all_entries"),
]
