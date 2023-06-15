from django.urls import path 
from .views import CaloView

url_patterns = [
    path("project",CaloView.as_view()),
    path("project/<int:id>",CaloView.as_view()),
]