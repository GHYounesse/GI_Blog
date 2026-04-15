from django.urls import path
from .views import (
    PostListAPIView,
    PostDetailAPIView,
    PostCreateAPIView,
    PostUpdateAPIView,
    PostDeleteAPIView,
    LikePostAPIView,
    ReadLaterAPIView,
    CommentCreateAPIView,
    CategorieCreateAPIView
)


urlpatterns = [
    path("categories/create/", CategorieCreateAPIView.as_view()),

    path("posts/", PostListAPIView.as_view()),
    path("posts/<int:pk>/", PostDetailAPIView.as_view()),
    path("posts/create/", PostCreateAPIView.as_view()),
    path("posts/<int:pk>/update/", PostUpdateAPIView.as_view()),
    path("posts/<int:pk>/delete/", PostDeleteAPIView.as_view()),

    path("posts/<int:pk>/like/", LikePostAPIView.as_view()),
    path("posts/<int:pk>/read-later/", ReadLaterAPIView.as_view()),
    path("posts/<int:pk>/comment/", CommentCreateAPIView.as_view()),

    
]
