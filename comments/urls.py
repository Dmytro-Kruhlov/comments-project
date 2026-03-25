from django.urls import path

from .views import CommentCreateAPIView, CommentRepliesAPIView, RootCommentListAPIView

urlpatterns = [
    path("comments/", RootCommentListAPIView.as_view(), name="comments-list"),
    path(
        "comments/<int:pk>/replies/",
        CommentRepliesAPIView.as_view(),
        name="comments-replies",
    ),
    path("comments/create/", CommentCreateAPIView.as_view(), name="comment-create"),
]
