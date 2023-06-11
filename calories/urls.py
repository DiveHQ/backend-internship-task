from django.urls import path

from .views import ( 
    CaloryView, 
    CaloryDetailsView, 
    GetCurrentCaloryDetails
)

urlpatterns = [
    path('<int:pk>/', CaloryView.as_view(), name='calory_view'),
    path('details/<int:pk>/', CaloryDetailsView.as_view(), name='calory_details_view'),
    path('current/', GetCurrentCaloryDetails.as_view(), name='todays_calory')
]