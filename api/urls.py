"""
URL mappings for the user API.
"""
from django.urls import path

from api.views import QueryView

urlpatterns = [
    path("query/", QueryView.as_view(), name="query"),
]
