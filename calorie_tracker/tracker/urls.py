from django.urls import path
from .views import *

urlpatterns = [
    path("entries/", entry_list, name="entry_list"),
    path("entries/<int:pk>/", entry_detail, name="entry_detail"),
]
