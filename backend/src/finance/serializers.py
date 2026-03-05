from rest_framework import serializers
from core.models.mixins.audit_serializer_mixin import AuditSerializerMixin
from finance.models import Transaction


class TransactionSerializer(AuditSerializerMixin):
    customer_id = serializers.CharField(source="customer.id", required=False, allow_null=True)
    customer_name = serializers.CharField(source="customer.name", read_only=True)
    type = serializers.ChoiceField(choices=Transaction.Type.choices)
    category = serializers.ChoiceField(choices=Transaction.Category.choices)
    payment_method = serializers.ChoiceField(choices=Transaction.PaymentMethod.choices)


    class Meta:
        model  = Transaction
        fields = [
            "id",
            "type",
            "category",
            "payment_method",
            "description",
            "value",
            "customer_id",
            "customer_name",
            "created_by",
            "created_at",
            "updated_at",
            "updated_by"
        ]
        read_only_fields = ["created_by", "created_at", "customer_name", "updated_at", "updated_by"]
    
    def create(self, validated_data):
        customer_data = validated_data.pop("customer", {})
        customer_id = customer_data.get("id")

        if customer_id is not None:
            validated_data["customer_id"] = customer_id

        return super().create(validated_data)

    def update(self, instance, validated_data):
        customer_data = validated_data.pop("customer", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if customer_data is not None:
            validated_data['customer_id'] = customer_data.get('id')

        return super().update(instance, validated_data)
