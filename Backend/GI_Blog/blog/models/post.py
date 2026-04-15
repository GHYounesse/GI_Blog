from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import humanize
from .categorie import Categorie
from .tag import Tag
from django.utils.text import slugify

class Post(models.Model):
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")
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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def total_likes(self):
        return self.liked.count()

    def read_check(self, pk):
        if self.read_later.filter(id=pk).exists():
            return True
        else:
            return False

    def time_published(self):
        return humanize.naturaltime(timezone.now() - self.date_posted)

