from django.db import models
from django.utils import timezone
from .post import Post
from django.contrib.auth.models import User
import humanize

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return str(self.author)

    def time_published(self):
        return humanize.naturaltime(timezone.now() - self.created_date)
