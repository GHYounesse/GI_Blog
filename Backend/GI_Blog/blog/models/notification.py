from django.db import models
from .post import Post
from .comment import Comment
from django.contrib.auth.models import User
class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ("like", "Like"),
        ("comment", "Comment"),
        ("reply", "Reply"),
    )

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_notifications")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")

    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)

    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({self.notification_type})"
