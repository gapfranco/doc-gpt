"""
URL configuration for hover project.
"""

# from django.shortcuts import redirect
from django.urls import path

from .views import (
    ask,
    delete_topic,
    document,
    edit_topic,
    frontpage,
    login,
    new_document,
    new_topic,
    qa,
    query,
    question,
    register,
    signout,
    topic,
)

urlpatterns = [
    # path("", lambda request: redirect("admin/", permanent=False)),
    path("", frontpage, name="frontpage"),
    path("new_topic", new_topic, name="new_topic"),
    path("topic/<str:topic_id>", topic, name="topic"),
    path("edit_topic/<str:topic_id>", edit_topic, name="edit_topic"),
    path("delete_topic/<str:topic_id>", delete_topic, name="delete_topic"),
    path("document/<str:topic_id>", document, name="document"),
    path("new_document/<str:topic_id>", new_document, name="new_document"),
    path("query/<str:topic_id>", query, name="query"),
    path("question/<str:topic_id>", question, name="question"),
    path("qa/<int:question_id>", qa, name="qa"),
    path("ask/<str:topic_id>", ask, name="ask"),
    path("login", login, name="login"),
    path("signout", signout, name="signout"),
    path("register", register, name="register"),
]
