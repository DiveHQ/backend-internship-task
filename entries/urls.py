from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateEntryView.as_view(), name='create_entry'),
    path('delete/', views.DeleteEntryView.as_view(), name='delete_entry'),
    path('update/', views.UpdateEntryView.as_view(), name='update_entry'),
    path('list/', views.ListEntriesView.as_view(), name='list_entries'),
    path('detail/', views.EntryDetailView.as_view(), name='get_entry'),
]