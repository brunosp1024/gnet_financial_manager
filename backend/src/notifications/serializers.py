from rest_framework import serializers
from core.serializers.audit_serializer_mixin import AuditSerializerMixin
from .models import Notification


class NotificationCreateSerializer(AuditSerializerMixin):

    class Meta:
        model = Notification
        fields = ["type", "message", "is_read"]


class NotificationListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ["id", "type", "message", "is_read", "created_at"]
