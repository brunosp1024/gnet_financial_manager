from rest_framework import serializers
from core.models.mixins.audit_serializer_mixin import AuditSerializerMixin
from finance.models import Transaction


class TransactionSerializer(AuditSerializerMixin):
    customer_id = serializers.CharField(source="customer.id")
    customer_name = serializers.CharField(source="customer.name", read_only=True)


    class Meta:
        model  = Transaction
        fields = [
            "type",
            "category",
            "payment_method",
            "description",
            "value",
            "date",
            "customer_id",
            "customer_name",
            "created_by",
            "created_at",
            "updated_at",
            "updated_by"
        ]
        read_only_fields = ["created_by", "created_at", "customer_name", "updated_at", "updated_by"]
