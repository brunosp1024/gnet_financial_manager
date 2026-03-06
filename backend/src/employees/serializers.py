from core.serializers.serializers import PersonSerializer
from employees.models import Employee


class EmployeeSerializer(PersonSerializer):
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
            "start_date",
            "observations",
            "is_active",
            "created_at",
            "created_by",
            "updated_at",
            "updated_by"
        ]
        read_only_fields = ["created_at", "created_by", "updated_at", "updated_by"]
