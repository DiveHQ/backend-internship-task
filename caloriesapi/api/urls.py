from django.urls import path
from . import views

urlpatterns = [
    path("account/create/", views.create_account),
    path("login/", views.login),
    path("entry/", views.create_calorie_entry),
    path("entry/<int:pk>", views.get_calorie_entry),
    path("entry/<int:pk>", views.update_calorie_entry),
    path("entry/<int:pk>", views.delete_calorie_entry),
    path("entries/", views.get_calorie_entries),
    path("entries/date", views.get_calorie_entries_by_date),
    path("entries/status", views.get_calorie_entries_by_status),
    path("users/", views.get_users),
]
