from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from core.permissions import GroupPermission
from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    search_fields = ['name', 'cpf', 'position']
    ordering_fields = ['name', 'position', 'admission_date', 'modality', 'created_at']
