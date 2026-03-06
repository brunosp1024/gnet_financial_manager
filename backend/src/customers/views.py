from rest_framework.viewsets import ModelViewSet
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.permissions import IsAuthenticated
from core.permissions import GroupPermission


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    search_fields = ['name', 'cpf', 'address']
    ordering_fields = ['name', 'start_date', 'created_at']
