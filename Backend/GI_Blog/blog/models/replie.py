from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .comment import Comment

class Replie(models.Model):
    comment = models.ForeignKey(Comment, related_name='replies', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)
    approved_replie = models.BooleanField(default=True)

    def approve(self):
        self.approved_replie = True
        self.save()

    def __str__(self):
        return str(self.author)

