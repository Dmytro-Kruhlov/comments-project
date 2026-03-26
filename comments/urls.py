from django.urls import path

from .views import (
    CaptchaAPIView,
    CommentCreateAPIView,
    CommentRepliesAPIView,
    RootCommentListAPIView,
    add_comment,
    index,
)

urlpatterns = [
    path("", index),
    path("add/", add_comment, name="add"),
    path("comments/", RootCommentListAPIView.as_view(), name="comments-list"),
    path(
        "comments/<int:pk>/replies/",
        CommentRepliesAPIView.as_view(),
        name="comments-replies",
    ),
    path("comments/create/", CommentCreateAPIView.as_view(), name="comment-create"),
    path("captcha/", CaptchaAPIView.as_view(), name="captcha"),
]
