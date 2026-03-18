from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from apps.core.serializers.audit_serializer_mixin import AuditSerializerMixin
from apps.users.models import User


class UserCreateSerializer(AuditSerializerMixin):
    password = serializers.CharField(write_only=True)
    group    = serializers.SlugRelatedField(
        queryset=Group.objects.all(),
        slug_field='name',
        write_only=True,
    )

    class Meta:
        model  = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "group",
            "password",
            "is_active",
        ]

    def create(self, validated_data):
        group = validated_data.pop("group")
        validated_data["created_by"] = self._current_user()
        validated_data["updated_by"] = self._current_user()
        user = User.objects.create_user(**validated_data)
        user.groups.set([group])
        return user

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("E-mail já está em uso.")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value


class UserDetailSerializer(AuditSerializerMixin):
    group = serializers.SerializerMethodField()

    class Meta:
        model  = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "group",
            "is_active",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]

    def get_group(self, obj) -> str | None:
        group = obj.groups.first()
        return group.name if group else None


class UserUpdateSerializer(AuditSerializerMixin):
    password = serializers.CharField(write_only=True, required=False)
    group    = serializers.SlugRelatedField(
        queryset=Group.objects.all(),
        slug_field='name',
        write_only=True,
        required=False,
    )

    class Meta:
        model  = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "group",
            "password",
            "is_active",
        ]

    def update(self, instance, validated_data):
        group    = validated_data.pop("group", None)
        password = validated_data.pop("password", None)

        instance = super().update(instance, validated_data)

        if group:
            instance.groups.set([group])

        if password:
            instance.set_password(password)
            instance.save(update_fields=["password"])

        return instance
    
    def validate_password(self, value):
        validate_password(value)
        return value

    def validate_email(self, value):
        qs = User.objects.exclude(pk=self.instance.pk).filter(email=value)
        if qs.exists():
            raise serializers.ValidationError("E-mail já está em uso.")
        return value

    def validate_username(self, value):
        qs = User.objects.exclude(pk=self.instance.pk).filter(username=value)
        if qs.exists():
            raise serializers.ValidationError("Username já está em uso.")
        return value


class UserListSerializer(AuditSerializerMixin):
    group = serializers.SerializerMethodField()

    class Meta:
        model  = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "group",
            "is_active",
            "created_at",
        ]

    def get_group(self, obj) -> str | None:
        group = obj.groups.first()
        return group.name if group else None
