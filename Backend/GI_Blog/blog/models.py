from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import math


class Categorie(models.Model):
    categorie_name = models.TextField()

    def __str__(self):
        return self.categorie_name

    def get_absolute_url(self):
        return reverse("index")


class Post(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to='social_media_pics')
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

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def total_likes(self):
        return self.liked.count()

    def read_check(self, pk):
        if self.read_later.filter(id=pk).exists():
            return True
        else:
            return False

    def time_published(self):

        time_difference = timezone.now() - self.date_posted

        if time_difference.days == 0 and 0 <= time_difference.seconds < 60:

            seconds = time_difference.seconds

            if seconds == 1:
                return f'{str(seconds)} second ago'

            else:
                return f'{str(seconds)} seconds ago'

        if time_difference.days == 0 and 60 <= time_difference.seconds < 3600:

            minutes = math.floor(time_difference.seconds / 60)

            if minutes == 1:
                return f'{str(minutes)} minute ago'
            else:
                return f'{str(minutes)} minutes ago'

        if time_difference.days == 0 and 3600 <= time_difference.seconds < 86400:

            hours = math.floor(time_difference.seconds / 3600)

            if hours == 1:
                return f'{str(hours)} hour ago'
            else:
                return f'{str(hours)} hours ago'

        if 1 <= time_difference.days < 30:

            days = time_difference.days

            if days == 1:
                return f'{str(days)} day ago'
            else:
                return f'{str(days)} days ago'

        if 30 <= time_difference.days < 365:

            months = math.floor(time_difference.days / 30)

            if months == 1:
                return f'{str(months)} month ago'
            else:
                return f'{str(months)} months ago'

        if time_difference.days >= 365:

            years = math.floor(time_difference.days / 365)

            if years == 1:
                return f'{str(years)} year ago'
            else:
                return f'{str(years)} years ago'


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("index")

    def __str__(self):
        return self.author

    def time_published(self):

        time_difference = timezone.now() - self.created_date

        if time_difference.days == 0 and 0 <= time_difference.seconds < 60:

            seconds = time_difference.seconds

            if seconds == 1:
                return f'{str(seconds)} second ago'

            else:
                return f'{str(seconds)} seconds ago'

        if time_difference.days == 0 and 60 <= time_difference.seconds < 3600:

            minutes = math.floor(time_difference.seconds / 60)

            if minutes == 1:
                return f'{str(minutes)} minute ago'
            else:
                return f'{str(minutes)} minutes ago'

        if time_difference.days == 0 and 3600 <= time_difference.seconds < 86400:

            hours = math.floor(time_difference.seconds / 3600)

            if hours == 1:
                return f'{str(hours)} hour ago'
            else:
                return f'{str(hours)} hours ago'

        if 1 <= time_difference.days < 30:

            days = time_difference.days

            if days == 1:
                return f'{str(days)} day ago'
            else:
                return f'{str(days)} days ago'

        if 30 <= time_difference.days < 365:

            months = math.floor(time_difference.days / 30)

            if months == 1:
                return f'{str(months)} month ago'
            else:
                return f'{str(months)} months ago'

        if time_difference.days >= 365:

            years = math.floor(time_difference.days / 365)

            if years == 1:
                return f'{str(years)} year ago'
            else:
                return f'{str(years)} years ago'


class Replie(models.Model):
    comment = models.ForeignKey(Comment, related_name='replies', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)
    approved_replie = models.BooleanField(default=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.author


class Message(models.Model):
    email = models.EmailField()
    object = models.CharField(max_length=100)
    content = models.TextField()

    def get_absolute_url(self):
        return reverse("index")

    def __str__(self):
        return self.object
