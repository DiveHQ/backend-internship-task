from django.urls import path 
from .views import CaloView

urlpatterns = [
    path("project",CaloView.as_view()),
    path("project/<int:id>",CaloView.as_view()),
]