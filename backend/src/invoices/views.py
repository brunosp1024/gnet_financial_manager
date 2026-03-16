from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from core.permissions import GroupPermission
from .models import Invoice
from .serializers import (
    InvoiceCreateSerializer,
    InvoiceUpdateSerializer,
    InvoiceListSerializer,
)


class InvoiceViewSet(ModelViewSet):
    queryset = Invoice.objects.select_related('customer')
    permission_resource = 'invoices'
    serializer_class = InvoiceListSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    ordering_fields = ['value', 'due_date', 'status', 'created_at']
    ordering = ['-due_date']
    serializer_classes = {
        'create': InvoiceCreateSerializer,
        'list': InvoiceListSerializer,
        'update': InvoiceUpdateSerializer,
        'partial_update': InvoiceUpdateSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)
