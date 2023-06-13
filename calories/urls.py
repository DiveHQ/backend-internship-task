from django.urls import path

from .views import ( 
    CaloryView, 
    CaloryDetailsView, 
    GetCurrentCaloryDetails,
    EditDeleteCaloryView
)

urlpatterns = [
    path('<int:pk>/', CaloryView.as_view(), name='calory_view'),
    path('get/<int:pk>/', CaloryDetailsView.as_view(), name='calory_details_view'),
    path('details/<int:pk>/', EditDeleteCaloryView.as_view(), name='edit_delete_calory'),
    path('current/', GetCurrentCaloryDetails.as_view(), name='todays_calory')
]