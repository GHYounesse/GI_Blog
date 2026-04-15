from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import math
import humanize


class Categorie(models.Model):
    categorie_name = models.TextField()

    def __str__(self):
        return self.categorie_name



class Post(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to='post_images')
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    liked = models.ManyToManyField(
        User, blank=True, related_name='liked')
    date_posted = models.DateTimeField(default=timezone.now)
    read_later = models.ManyToManyField(
        User, blank=True, related_name='read_later')

    class Meta:
        ordering = ('-date_posted',)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.liked.count()

    def read_check(self, pk):
        if self.read_later.filter(id=pk).exists():
            return True
        else:
            return False

    def time_published(self):
        return humanize.naturaltime(timezone.now() - self.date_posted)


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


class Message(models.Model):
    email = models.EmailField()
    object = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.object
