# Generated by Django 4.0.2 on 2022-04-19 15:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0002_post_read_later'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='read_later',
        ),
        migrations.AddField(
            model_name='post',
            name='read_later',
            field=models.ManyToManyField(blank=True, related_name='read_later', to=settings.AUTH_USER_MODEL),
        ),
    ]