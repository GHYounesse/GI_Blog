from django.contrib import admin
from .models import Post, Comment, Categorie

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Categorie)

admin.site.site_header = " Admin Page"
admin.site.site_title = "Custom bookstore admin site"
admin.site.index_title = "Custom Bookstore Admin"
