from rest_framework import serializers
from core.serializers.serializers import PersonSerializer
from customers.models import Customer


class CustomerCreateUpdateSerializer(PersonSerializer):
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
            "created_by",
            "updated_by",
        ]

class CustomerDetailSerializer(PersonSerializer):
    is_overdue = serializers.BooleanField(read_only=True)

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
            "is_overdue",
            "created_at",
            "created_by",
            "updated_at",
            "updated_by"
        ]

class CustomerListSerializer(PersonSerializer):
    is_overdue = serializers.BooleanField(read_only=True)

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
            "is_overdue",
            "created_at",
            "created_by",
            "updated_at",
            "updated_by"
        ]
