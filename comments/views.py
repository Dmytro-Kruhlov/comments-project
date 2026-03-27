import uuid

from django.core.cache import cache
from django.shortcuts import render
from rest_framework import filters, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .captcha import generate_captcha
from .models import Comment
from .pagination import CommentPagination, ReplyPagination
from .serializers import CommentCreateSerializer, CommentListSerializer, ReplySerializer


def index(request):
    return render(request, "index.html")


def add_comment(request):
    return render(request, "add.html")


class RootCommentListAPIView(generics.ListAPIView):

    queryset = Comment.objects.filter(parent=None)
    serializer_class = CommentListSerializer
    pagination_class = CommentPagination

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["username", "email", "created_at"]
    ordering = ["-created_at"]


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


class CaptchaAPIView(APIView):
    def get(self, request):
        text, image = generate_captcha()

        captcha_id = str(uuid.uuid4())

        cache.set(captcha_id, text, timeout=300)

        return Response({"captcha_id": captcha_id, "image": image})
