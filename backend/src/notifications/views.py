from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from core.permissions import GroupPermission
from .models import Notification
from .serializers import NotificationCreateSerializer, NotificationListSerializer


class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    permission_resource = 'notifications'
    serializer_class = NotificationListSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_read", "type"]
    serializer_classes = {
        'create': NotificationCreateSerializer,
        'list': NotificationListSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)
