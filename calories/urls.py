from django.urls import path

from .views import (
    CaloryLimitView, 
    CaloryLimitDetailsView, 
    CaloryView, 
    CaloryDetailsView, 
    GetCurrentCaloryDetails
)

urlpatterns = [
    path('limit/', CaloryLimitView.as_view(), name='calory_limit'),
    path('limit/<int:pk>/', CaloryLimitDetailsView.as_view(), name='calory_limit_details'),
    path('<int:pk>/', CaloryView.as_view(), name='calory_view'),
    path('details/<int:pk>/', CaloryDetailsView.as_view(), name='calory_details_view'),
    path('current/', GetCurrentCaloryDetails.as_view(), name='todays_calory')
]