"""
URL configuration for hover project.
"""

# from django.shortcuts import redirect
from django.urls import path

from .views import (  # qa,; question,
    ask,
    chat,
    chat_delete,
    chat_detail,
    delete_invite,
    delete_topic,
    delete_user_account,
    doc_summary,
    document,
    edit_topic,
    empty,
    frontpage,
    login,
    main,
    new_document,
    new_invite,
    new_topic,
    profile,
    publish,
    publish_topic,
    query,
    register,
    send_invite,
    signout,
    stripe,
    topic,
)

urlpatterns = [
    # path("", lambda request: redirect("admin/", permanent=False)),
    path("", main, name="frontpage"),
    path("empty", empty, name="empty"),
    path("main", frontpage, name="main"),
    path("profile", profile, name="profile"),
    path("stripe", stripe, name="stripe"),
    path("new_topic", new_topic, name="new_topic"),
    path("topic/<str:topic_id>", topic, name="topic"),
    path("edit_topic/<str:topic_id>", edit_topic, name="edit_topic"),
    path("delete_topic/<str:topic_id>", delete_topic, name="delete_topic"),
    path(
        "delete_invite/<str:topic_id>/<str:invite_id>",
        delete_invite,
        name="delete_invite",
    ),
    path(
        "send_invite/<str:topic_id>/<str:invite_id>",
        send_invite,
        name="send_invite",
    ),
    path("document/<str:topic_id>", document, name="document"),
    path("doc_summary/<str:doc_id>", doc_summary, name="doc_summary"),
    path("publish/<str:topic_id>", publish, name="publish"),
    path("new_invite/<str:topic_id>", new_invite, name="new_invite"),
    path("publish_topic/<str:topic_id>", publish_topic, name="publish_topic"),
    path("new_document/<str:topic_id>", new_document, name="new_document"),
    path("query/<str:topic_id>", query, name="query"),
    # path("question/<str:topic_id>", question, name="question"),
    path("chat/<str:topic_id>", chat, name="chat"),
    path("chat_detail/<int:question_id>", chat_detail, name="chat_detail"),
    path("chat_delete/<int:id>", chat_delete, name="chat_delete"),
    # path("qa/<int:question_id>", qa, name="qa"),
    path("ask/<str:topic_id>", ask, name="ask"),
    path("login", login, name="login"),
    path("signout", signout, name="signout"),
    path("register", register, name="register"),
    path("delete_account/", delete_user_account, name="delete_account"),
]
