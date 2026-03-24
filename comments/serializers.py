from rest_framework import serializers

from .models import Comment


class CommentListSerializer(serializers.ModelSerializer):
    first_reply = serializers.SerializerMethodField()

    def get_first_reply(self, obj):
        first = obj.replies.all()[:1]
        return ReplySerializer(first, many=True).data

    class Meta:
        model = Comment
        fields = ["id", "username", "text", "created_at", "first_reply"]


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "username", "text", "created_at"]
