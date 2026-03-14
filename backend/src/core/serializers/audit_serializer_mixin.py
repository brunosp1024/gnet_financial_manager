from rest_framework import serializers


class AuditSerializerMixin(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    def get_created_by(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None

    def get_updated_by(self, obj):
        return obj.updated_by.get_full_name() if obj.updated_by else None

    def _current_user(self):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user
        return None

    def create(self, validated_data):
        validated_data['created_by'] = self._current_user()
        validated_data['updated_by'] = self._current_user()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self._current_user()
        return super().update(instance, validated_data)