from rest_framework import viewsets, permissions
from ..models.notification import Notification
from ..serializers import NotificationSerializer
from rest_framework.decorators import action

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user).select_related("sender", "post", "comment")

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
    
    
    @action(detail=True, methods=["post"])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({"status": "read"})
    
    @action(detail=False, methods=["get"])
    def unread_count(self, request):
        count = Notification.objects.filter(
            receiver=request.user,
            is_read=False
        ).count()
        return Response({"unread": count})