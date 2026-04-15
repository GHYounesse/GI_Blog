from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from ..models import Post
from ..serializers import PostSerializer, CommentSerializer
from ..permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        qs = Post.objects.all()

        q = self.request.query_params.get("q")
        if q:
            qs = qs.filter(title__icontains=q) | qs.filter(content__icontains=q)

        return qs.select_related("author", "categorie").prefetch_related("comments")

    # 🔥 LIKE TOGGLE
    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()

        if request.user in post.liked.all():
            post.liked.remove(request.user)
            return Response({"liked": False})

        post.liked.add(request.user)
        return Response({"liked": True})

    # 🔥 READ LATER TOGGLE
    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def read_later(self, request, pk=None):
        post = self.get_object()

        if request.user in post.read_later.all():
            post.read_later.remove(request.user)
            return Response({"saved": False})

        post.read_later.add(request.user)
        return Response({"saved": True})

    # 🔥 CREATE COMMENT INSIDE POST
    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def comment(self, request, pk=None):
        post = self.get_object()

        text = request.data.get("text")
        if not text:
            return Response({"error": "Text required"}, status=400)

        comment = post.comments.create(
            author=request.user,
            text=text
        )

        return Response({"message": "Comment added", "id": comment.id})
