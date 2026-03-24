from rest_framework import serializers

from .models import Comment


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
