import re

import bleach
from rest_framework import serializers

from .models import Comment

ALLOWED_TAGS = {"a", "code", "i", "strong"}
ALLOWED_ATTRIBUTES = {
    "a": ["href", "title"],
}


class CommentListSerializer(serializers.ModelSerializer):
    first_reply = serializers.SerializerMethodField()

    def get_first_reply(self, obj):
        reply = obj.replies.order_by("created_at").first()
        if reply:
            return ReplySerializer(reply).data
        return None

    class Meta:
        model = Comment
        fields = ["id", "username", "text", "created_at", "first_reply"]


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "username", "text", "created_at"]


class CommentCreateSerializer(serializers.ModelSerializer):
    text = serializers.CharField(allow_blank=True)

    class Meta:
        model = Comment
        fields = ("username", "email", "homepage", "text", "parent")
        extra_kwargs = {"parent": {"required": False, "allow_null": True}}

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Text cannot be empty")

        cleaned = bleach.clean(
            value,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=True,
        )

        return cleaned

    def validate_username(self, value):
        if not re.match(r"^[a-zA-Z0-9]+$", value):
            raise serializers.ValidationError("Only latin letters and digits allowed")
        return value
