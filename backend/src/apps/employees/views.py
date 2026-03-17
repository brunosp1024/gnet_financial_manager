from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from apps.core.permissions import GroupPermission
from .models import Employee
from .serializers import EmployeeListSerializer, EmployeeDetailSerializer, EmployeeCreateUpdateSerializer


class EmployeeViewSet(ModelViewSet):
    permission_resource = 'employees'
    queryset = Employee.objects.all()
    serializer_class = EmployeeListSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    search_fields = ['name', 'cpf', 'position']
    ordering_fields = ['name', 'position', 'start_date', 'modality', 'created_at']
    serializer_classes = {
        'create': EmployeeCreateUpdateSerializer,
        'list': EmployeeListSerializer,
        'retrieve': EmployeeDetailSerializer,
        'update': EmployeeCreateUpdateSerializer,
        'partial_update': EmployeeCreateUpdateSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)
