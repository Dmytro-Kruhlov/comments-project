import re

import bleach
from django.core.cache import cache
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
    captcha_id = serializers.CharField(write_only=True)
    captcha = serializers.CharField(write_only=True)

    class Meta:
        model = Comment
        fields = (
            "username",
            "email",
            "homepage",
            "text",
            "parent",
            "captcha_id",
            "captcha",
        )
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

    def validate(self, attrs):
        captcha_id = attrs.get("captcha_id")
        captcha_value = attrs.get("captcha")

        real_value = cache.get(captcha_id)

        if not real_value:
            raise serializers.ValidationError("Captcha expired")

        if captcha_value.lower() != real_value.lower():
            raise serializers.ValidationError("Invalid captcha")

        return attrs

    def create(self, validated_data):

        validated_data.pop("captcha_id", None)
        validated_data.pop("captcha", None)
        return super().create(validated_data)
