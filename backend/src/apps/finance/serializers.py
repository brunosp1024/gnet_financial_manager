from rest_framework import serializers
from apps.core.serializers.audit_serializer_mixin import AuditSerializerMixin
from apps.finance.models import Transaction


class TransactionCreateSerializer(AuditSerializerMixin):
    customer_id = serializers.UUIDField(required=False, allow_null=True)
    type = serializers.ChoiceField(choices=Transaction.Type.choices)
    category = serializers.ChoiceField(choices=Transaction.Category.choices)
    payment_method = serializers.ChoiceField(choices=Transaction.PaymentMethod.choices, required=False, allow_blank=True)

    class Meta:
        model  = Transaction
        fields = [
            "type",
            "category",
            "payment_method",
            "customer_id",
            "description",
            "value",
        ]

    def validate(self, attrs):
        transaction_type = attrs.get("type")
        payment_method = attrs.get("payment_method", "")
        category = attrs.get("category")

        if transaction_type == Transaction.Type.INCOME and not payment_method:
            raise serializers.ValidationError({"payment_method": "Obrigatório para entradas."})

        income_categories = {Transaction.Category.MONTHLY_FEE, Transaction.Category.STORE_SERVICE}
        expense_categories = {Transaction.Category.LOGISTIC, Transaction.Category.PAYROLL}

        if transaction_type == Transaction.Type.INCOME and category not in income_categories:
            raise serializers.ValidationError({"category": "Categoria inválida para entradas."})
        if transaction_type == Transaction.Type.EXPENSE and category not in expense_categories:
            raise serializers.ValidationError({"category": "Categoria inválida para despesas."})

        return attrs


class TransactionUpdateSerializer(TransactionCreateSerializer):

    def validate(self, attrs):
        instance = self.instance
        attrs.setdefault("type", instance.type)
        attrs.setdefault("payment_method", instance.payment_method)
        attrs.setdefault("category", instance.category)
        return super().validate(attrs)


class TransactionListSerializer(AuditSerializerMixin):
    customer_name = serializers.CharField(source="customer.name", read_only=True)
    type_display = serializers.CharField(source="get_type_display", read_only=True)
    category_display = serializers.CharField(source="get_category_display", read_only=True)

    class Meta:
        model  = Transaction
        fields = [
            "id",
            "type_display",
            "category_display",
            "payment_method",
            "customer_name",
            "description",
            "value",
            "created_at",
        ]


class TransactionDetailSerializer(AuditSerializerMixin):
    customer_id = serializers.UUIDField(source="customer.id", read_only=True)
    customer_name = serializers.CharField(source="customer.name", read_only=True)
    type_display = serializers.CharField(source="get_type_display", read_only=True)
    category_display = serializers.CharField(source="get_category_display", read_only=True)
    created_by_name = serializers.CharField(source="created_by.get_full_name", read_only=True)
    updated_by_name = serializers.CharField(source="updated_by.get_full_name", read_only=True)

    class Meta:
        model  = Transaction
        fields = [
            "id",
            "type_display",
            "category_display",
            "payment_method",
            "customer_id",
            "customer_name",
            "description",
            "value",
            "created_at",
            "updated_at",
            "created_by_name",
            "updated_by_name",
        ]
