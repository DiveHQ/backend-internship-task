from django.urls import path

from .views import (
    CaloryLimitView,
    CaloryLimitDetailsView
)

urlpatterns = [
    path('', CaloryLimitView.as_view(), name='calory_limit'),
    path('<int:pk>/', CaloryLimitDetailsView.as_view(), name='calory_limit_details'),

]