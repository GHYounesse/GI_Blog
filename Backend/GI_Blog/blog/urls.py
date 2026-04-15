from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.post import PostViewSet
from .views.category import CategoryViewSet
from .views.comment import CommentViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]
