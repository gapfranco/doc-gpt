"""
URL configuration for hover project.
"""

# from django.shortcuts import redirect
from django.urls import path

from .views import (
    ask,
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
    path("topic/<str:topic_id>", topic, name="topic"),
    path("document/<str:topic_id>", document, name="document"),
    path("new_document/<str:topic_id>", new_document, name="new_document"),
    path("ask/<str:topic_id>", ask, name="ask"),
    path("login", login, name="login"),
    path("signout", signout, name="signout"),
    path("register", register, name="register"),
]