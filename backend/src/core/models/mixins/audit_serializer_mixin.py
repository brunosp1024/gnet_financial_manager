from rest_framework import serializers


class AuditSerializerMixin(serializers.ModelSerializer):
    created_by = serializers.CharField(source="created_by.get_full_name", read_only=True)
    updated_by = serializers.CharField(source="updated_by.get_full_name", read_only=True)

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