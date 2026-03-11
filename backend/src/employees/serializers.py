from core.serializers.serializers import PersonSerializer
from employees.models import Employee


class EmployeeCreateUpdateSerializer(PersonSerializer):
    class Meta:
        model = Employee
        fields = [
            "name",
            "address",
            "phone",
            "cpf",
            "position",
            "modality",
            "birthday",
            "start_date",
            "observations",
            "is_active",
        ]

class EmployeeDetailSerializer(PersonSerializer):
    class Meta:
        model = Employee
        fields = [
            "id",
            "name",
            "address",
            "phone",
            "cpf",
            "position",
            "modality",
            "birthday",
            "start_date",
            "observations",
            "is_active",
            "created_at",
            "created_by",
            "updated_at",
            "updated_by"
        ]

class EmployeeListSerializer(PersonSerializer):
    class Meta:
        model = Employee
        fields = [
            "id",
            "name",
            "phone",
            "position",
            "modality",
            "start_date",
            "is_active",
        ]
