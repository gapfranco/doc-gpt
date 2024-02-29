"""
URL configuration for hover project.
"""

# from django.shortcuts import redirect
from django.urls import path

from .views import frontpage, signin, signout

urlpatterns = [
    # path("", lambda request: redirect("admin/", permanent=False)),
    path("", frontpage, name="frontpage"),
    path("signin", signin, name="signin"),
    path("signout", signout, name="signout"),
]
