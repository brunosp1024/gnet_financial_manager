from rest_framework.viewsets import ModelViewSet
from .models import Customer
from .serializers import CustomerCreateUpdateSerializer, CustomerListSerializer, CustomerDetailSerializer
from .filters import CustomerFilter
from rest_framework.permissions import IsAuthenticated
from core.permissions import GroupPermission
from django.db.models import Exists, OuterRef
from invoices.models import Invoice


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerListSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    search_fields = ['name', 'cpf', 'address']
    ordering_fields = ['name', 'start_date', 'created_at']
    filterset_class = CustomerFilter
    serializer_classes = {
        'create': CustomerCreateUpdateSerializer,
        'list': CustomerListSerializer,
        'retrieve': CustomerDetailSerializer,
        'update': CustomerCreateUpdateSerializer,
        'partial_update': CustomerCreateUpdateSerializer
    }

    def get_queryset(self):
        return Customer.objects.annotate(
            is_overdue=Exists(
                Invoice.objects.filter(
                    customer=OuterRef("pk"),
                    status=Invoice.Status.OVERDUE
                )
            )
        )

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)
