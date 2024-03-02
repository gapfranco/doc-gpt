"""
URL configuration for hover project.
"""

# from django.shortcuts import redirect
from django.urls import path

from .views import frontpage, login, new_topic, register, signout, topic

urlpatterns = [
    # path("", lambda request: redirect("admin/", permanent=False)),
    path("", frontpage, name="frontpage"),
    path("new_topic", new_topic, name="new_topic"),
    path("topic/<int:topic_id>", topic, name="topic"),
    path("login", login, name="login"),
    path("signout", signout, name="signout"),
    path("register", register, name="register"),
]
