from rest_framework import viewsets, permissions
from ..models.comment import Comment
from ..serializers import CommentSerializer
from ..permissions import IsAuthorOrReadOnly,IsAuthorOrModeratorOrAdmin


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrModeratorOrAdmin
    ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
