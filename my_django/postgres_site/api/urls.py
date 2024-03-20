from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
import requests

urlpatterns = [
    path("path_check/", views.PathList.as_view(), name="path_lister"),
    path(
        "path_check/<int:pk>/",
        views.PathRetrieveUpdateDestory.as_view(),
        name="update",
    ),
    path("path_check/detail/<int:pk>", views.path_detail, name="path_getter"),

    
]


