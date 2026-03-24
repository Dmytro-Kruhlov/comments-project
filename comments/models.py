from django.db import models
from django.utils import timezone


class Comment(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    homepage = models.URLField(blank=True, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.username}: {str(self.text)[:20]}"
