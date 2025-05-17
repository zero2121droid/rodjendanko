from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from notifications.models import Notification
from api.serializers.s_notifications import NotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'message']
    ordering_fields = ['created_at', 'is_read']
    filterset_fields = ['is_read']

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by("created_at")

    def perform_create(self, serializer):
        serializer.save(recipient=self.request.user)
