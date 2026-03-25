from rest_framework import generics

from .models import Comment
from .pagination import CommentPagination, ReplyPagination
from .serializers import CommentCreateSerializer, CommentListSerializer, ReplySerializer


class RootCommentListAPIView(generics.ListAPIView):

    queryset = Comment.objects.filter(parent=None).order_by("-created_at")
    serializer_class = CommentListSerializer
    pagination_class = CommentPagination


class CommentRepliesAPIView(generics.ListAPIView):

    serializer_class = ReplySerializer
    pagination_class = ReplyPagination

    def get_queryset(self):
        parent_id = self.kwargs["pk"]
        first_reply = (
            Comment.objects.filter(parent_id=parent_id).order_by("created_at").first()
        )
        if first_reply:
            return (
                Comment.objects.filter(parent_id=parent_id)
                .exclude(id=first_reply.id)
                .order_by("created_at")
            )
        return Comment.objects.filter(parent_id=parent_id).order_by("created_at")


class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer
    queryset = Comment.objects.all()
