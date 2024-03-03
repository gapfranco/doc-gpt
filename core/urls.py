"""
URL configuration for hover project.
"""

# from django.shortcuts import redirect
from django.urls import path

from .views import (
    document,
    frontpage,
    login,
    new_document,
    new_topic,
    register,
    signout,
    topic,
)

urlpatterns = [
    # path("", lambda request: redirect("admin/", permanent=False)),
    path("", frontpage, name="frontpage"),
    path("new_topic", new_topic, name="new_topic"),
    path("topic/<int:topic_id>", topic, name="topic"),
    path("document/<int:topic_id>", document, name="document"),
    path("new_document/<int:topic_id>", new_document, name="new_document"),
    path("login", login, name="login"),
    path("signout", signout, name="signout"),
    path("register", register, name="register"),
]
