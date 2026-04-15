from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user

from rest_framework.generics import ListAPIView
from .models import Post,Comment
from .serializers import PostSerializer,CategorySerializer
from django.db.models import Q
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import UpdateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
class CategorieCreateAPIView(CreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    

class PostListAPIView(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        keyword = self.request.GET.get("q", "")
        if keyword:
            return Post.objects.filter(
                Q(title__icontains=keyword) |
                Q(content__icontains=keyword)).select_related('author', 'categorie')
            
        return Post.objects.all()
        
    def get_serializer_context(self):
        return {"request": self.request}



class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostCreateAPIView(CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class PostUpdateAPIView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]



class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]


class LikePostAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        if request.user in post.liked.all():
            post.liked.remove(request.user)
            liked = False
        else:
            post.liked.add(request.user)
            liked = True

        return Response({"liked": liked})

class ReadLaterAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        if post.read_later.filter(id=request.user.id).exists():
            post.read_later.remove(request.user)
            return Response({"saved": False})
        else:
            post.read_later.add(request.user)
            return Response({"saved": True})


class CommentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        text = request.data.get("text")
        if not text:
            return Response({"error": "Text is required"}, status=400)

        comment = Comment.objects.create(
            author=request.user,
            post=post,
            text=text
        )

        return Response({"message": "Comment added"})

