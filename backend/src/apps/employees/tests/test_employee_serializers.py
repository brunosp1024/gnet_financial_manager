import pytest
from apps.employees.serializers import (
    EmployeeCreateUpdateSerializer,
    EmployeeDetailSerializer,
    EmployeeListSerializer
)
from apps.employees.tests.factories import EmployeeFactory
from rest_framework.test import APIRequestFactory


def make_request(user):
    factory = APIRequestFactory()
    req = factory.post('/')
    req.user = user
    return req


@pytest.mark.django_db
class TestEmployeeSerializer:

    # ======= Validation cpf tests =======
    def test_duplicate_cpf_is_rejected(self, admin_user):
        EmployeeFactory(cpf='52998224725')
        data = {
            'name':       'Another Employee',
            'cpf':        '52998224725',
            'start_date': '2024-01-01',
        }
        serializer = EmployeeCreateUpdateSerializer(data=data, context={'request': make_request(admin_user)})
        assert not serializer.is_valid()
        assert 'cpf' in serializer.errors

    def test_duplicate_cpf_allows_updating_same_record(self, admin_user):
        employee = EmployeeFactory(cpf='52998224725')
        data = {'cpf': '52998224725', 'name': 'Updated Name'}
        serializer = EmployeeCreateUpdateSerializer(
            employee, data=data, partial=True,
            context={'request': make_request(admin_user)},
        )
        assert serializer.is_valid(), serializer.errors


    # ======= Validation phone tests =======
    def test_duplicated_phone_is_rejected(self, admin_user):
        EmployeeFactory(phone='11912345678')
        data = {'name': 'Another Employee', 'start_date': '2024-01-01', 'phone': '11912345678'}
        serializer = EmployeeCreateUpdateSerializer(data=data, context={'request': make_request(admin_user)})
        assert not serializer.is_valid()
        assert 'phone' in serializer.errors

    def test_duplicated_phone_allows_updating_same_record(self, admin_user):
        employee = EmployeeFactory(phone='11912345678')
        data = {'phone': '11912345678', 'name': 'Updated Name'}
        serializer = EmployeeCreateUpdateSerializer(
            employee, data=data, partial=True,
            context={'request': make_request(admin_user)},
        )
        assert serializer.is_valid(), serializer.errors
    
    # ======= Validation EmployeeCreateUpdateSerializer tests =======
    def test_employee_create_update_serializer_successes(self, admin_user):
        employee = EmployeeFactory(phone='11912345678')
        data = {'name': 'New Employee', 'start_date': '2024-01-01'}
        serializer = EmployeeCreateUpdateSerializer(data=data, context={'request': make_request(admin_user)})
        assert serializer.is_valid(), serializer.errors

        phone = '11987654321'
        employee.phone = phone
        serializer = EmployeeCreateUpdateSerializer(employee, data={'phone': phone}, partial=True, context={'request': make_request(admin_user)})
        assert serializer.is_valid(), serializer.errors
        assert serializer.save().phone == phone
    
    # ======= Validation EmployeeDetailSerializer tests =======
    def test_employee_detail_serializer_displays_audit_fields(self, admin_user):
        employee = EmployeeFactory()
        employee.created_by = admin_user
        employee.updated_by = admin_user
        employee.save()
        serializer = EmployeeDetailSerializer(employee, context={'request': make_request(admin_user)})
        expected = {
            "id", "name", "address", "phone", "cpf", "position", "modality", "start_date", "birthday",
            "observations", "is_active", "created_at", "created_by", "updated_at", "updated_by"
        }
        assert expected == set(serializer.data.keys())
    
    # ======= Validation EmployeeListSerializer tests =======
    def test_employee_list_serializer_displays_fields(self, admin_user):
        employee = EmployeeFactory()
        serializer = EmployeeListSerializer(employee, context={'request': make_request(admin_user)})
        expected = {"id", "name", "phone", "position", "modality", "start_date", "is_active"}
        assert expected == set(serializer.data.keys())

    def test_employee_list_serializer_with_many(self, admin_user):
        EmployeeFactory.create_batch(3)
        from apps.employees.models import Employee
        qs = Employee.objects.all()
        serializer = EmployeeListSerializer(qs, many=True, context={'request': make_request(admin_user)})
        assert len(serializer.data) == 3
