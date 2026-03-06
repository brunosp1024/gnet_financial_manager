from core.serializers.serializers import PersonSerializer
from customers.models import Customer


class CustomerSerializer(PersonSerializer):
    class Meta:
        model  = Customer
        fields = [
            "id",
            "name",
            "address",
            "phone",
            "cpf",
            "start_date",
            "birthday",
            "observations",
            "is_active",
            "created_at",
            "created_by",
            "updated_at",
            "updated_by"
        ]
        read_only_fields = ["created_at", "created_by", "updated_at", "updated_by"]
