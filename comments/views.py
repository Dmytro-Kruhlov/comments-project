from rest_framework import generics

from .models import Comment
from .pagination import CommentPagination, ReplyPagination
from .serializers import CommentListSerializer, ReplySerializer


class RootCommentListAPIView(generics.ListAPIView):

    queryset = Comment.objects.filter(parent=None).order_by("-created_at")
    serializer_class = CommentListSerializer
    pagination_class = CommentPagination


class CommentRepliesAPIView(generics.ListAPIView):

    serializer_class = ReplySerializer
    pagination_class = ReplyPagination

    def get_queryset(self):
        parent_id = self.kwargs["pk"]
        return Comment.objects.filter(parent_id=parent_id).order_by("created_at")
