from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from ..models.post import Post
from ..models.notification import Notification
from ..serializers import PostSerializer, CommentSerializer
from ..permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    filterset_fields = ["categorie", "author"]
    ordering_fields = ["date_posted", "title"]
    ordering = ["-date_posted"]
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        qs = Post.objects.select_related("author", "categorie") \
                        .prefetch_related("comments", "liked", "read_later")

        q = self.request.query_params.get("q")
        category = self.request.query_params.get("category")
        author = self.request.query_params.get("author")

        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(content__icontains=q)
            )

        if category:
            qs = qs.filter(categorie__categorie_name__icontains=category)

        if author:
            qs = qs.filter(author__username__icontains=author)

        return qs
    # 🔥 LIKE TOGGLE
    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        liked = post.liked.filter(id=request.user.id).exists()
        if liked:
            post.liked.remove(request.user)
            return Response({"liked": False})

        post.liked.add(request.user)
        if post.author != request.user:
            Notification.objects.create(
                sender=request.user,
                receiver=post.author,
                notification_type="like",
                post=post
            )
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
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user, post=post)
        if post.author != request.user:
            Notification.objects.create(
                sender=request.user,
                receiver=post.author,
                notification_type="comment",
                post=post,
                comment=comment
            )
        return Response(serializer.data)
        # text = request.data.get("text")
        # if not text:
        #     return Response({"error": "Text required"}, status=400)

        # comment = post.comments.create(
        #     author=request.user,
        #     text=text
        # )

        # return Response({"message": "Comment added", "id": comment.id})

    @action(detail=True, methods=["get"])
    def comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comments.select_related("author").prefetch_related("replies")
        serializer = CommentSerializer(comments, many=True, context={"request": request})
        return Response(serializer.data)