from rest_framework import serializers
from django.utils import timezone
from core.serializers.audit_serializer_mixin import AuditSerializerMixin
from invoices.models import Invoice


class InvoiceCreateSerializer(AuditSerializerMixin):
    customer_id = serializers.UUIDField()

    class Meta:
        model = Invoice
        fields = [
            "id",
            "customer_id",
            "value",
            "due_date"
        ]
        read_only_fields = ["id"]


class InvoiceUpdateSerializer(AuditSerializerMixin):
    status = serializers.ChoiceField(
        choices=Invoice.Status.choices,
        default=Invoice.Status.PENDING,
    )

    class Meta:
        model = Invoice
        fields = [
            "value",
            "due_date",
            "status",
            "paid_at",
        ]

    def validate(self, attrs):
        instance = self.instance
        attrs.setdefault("status", instance.status)

        if attrs["status"] == Invoice.Status.PAID and not attrs.get("paid_at"):
            attrs["paid_at"] = timezone.localdate()

        return super().validate(attrs)


class InvoiceListSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.name", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Invoice
        fields = [
            "id",
            "customer_name",
            "value",
            "due_date",
            "status",
            "status_display",
            "paid_at"
        ]
