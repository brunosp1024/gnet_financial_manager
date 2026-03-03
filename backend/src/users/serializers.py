from rest_framework import serializers
from core.models.mixins.audit_serializer_mixin import AuditSerializerMixin
from users.models import User


class UserSerializer(AuditSerializerMixin):
    password = serializers.CharField(write_only=True)

    class Meta:
        model  = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "is_active",
            "created_at",
            "created_by",
            "updated_at",
            "updated_by"
        ]
        read_only_fields = ["created_at", "created_by", "updated_at", "updated_by"]

    def create(self, validated_data):
        current_user = self._current_user()
        validated_data["created_by"] = current_user
        validated_data["updated_by"] = current_user
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        instance = super().update(instance, validated_data)

        if password:
            instance.set_password(password)
            instance.save(update_fields=["password"])

        return instance
