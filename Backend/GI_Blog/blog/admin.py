from django.contrib import admin
from .models import Post, Comment, Categorie


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "categorie", "date_posted")
    search_fields = ("title", "content")
    list_filter = ("categorie", "date_posted")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "post", "created_date", "approved_comment")
    search_fields = ("text",)
    list_filter = ("approved_comment",)


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ("categorie_name",)
