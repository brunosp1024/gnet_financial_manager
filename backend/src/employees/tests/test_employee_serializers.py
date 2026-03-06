import pytest
from employees.serializers import EmployeeSerializer
from employees.tests.factories import EmployeeFactory
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
        serializer = EmployeeSerializer(data=data, context={'request': make_request(admin_user)})
        assert not serializer.is_valid()
        assert 'cpf' in serializer.errors

    def test_duplicate_cpf_allows_updating_same_record(self, admin_user):
        employee = EmployeeFactory(cpf='52998224725')
        data = {'cpf': '52998224725', 'name': 'Updated Name'}
        serializer = EmployeeSerializer(
            employee, data=data, partial=True,
            context={'request': make_request(admin_user)},
        )
        assert serializer.is_valid(), serializer.errors


    # ======= Validation phone tests =======
    def test_duplicated_phone_is_rejected(self, admin_user):
        EmployeeFactory(phone='11912345678')
        data = {'name': 'Another Employee', 'start_date': '2024-01-01', 'phone': '11912345678'}
        serializer = EmployeeSerializer(data=data, context={'request': make_request(admin_user)})
        assert not serializer.is_valid()
        assert 'phone' in serializer.errors

    def test_duplicated_phone_allows_updating_same_record(self, admin_user):
        employee = EmployeeFactory(phone='11912345678')
        data = {'phone': '11912345678', 'name': 'Updated Name'}
        serializer = EmployeeSerializer(
            employee, data=data, partial=True,
            context={'request': make_request(admin_user)},
        )
        assert serializer.is_valid(), serializer.errors
