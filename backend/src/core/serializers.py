from rest_framework import serializers
from core.models.mixins.audit_serializer_mixin import AuditSerializerMixin
from utils.validators import validate_cpf as validate_cpf_util


class PersonSerializer(AuditSerializerMixin):
    def validate_cpf(self, value):
        if not value:
            return value

        validate_cpf_util(value)

        qs = self.Meta.model.objects.filter(cpf=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('CPF já cadastrado no sistema.')

        return value
