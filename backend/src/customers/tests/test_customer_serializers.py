import pytest
from customers.serializers import CustomerSerializer
from customers.tests.factories import CustomerFactory
from rest_framework.test import APIRequestFactory


def make_request(user):
    factory = APIRequestFactory()
    req = factory.post('/')
    req.user = user
    return req


@pytest.mark.django_db
class TestCustomerSerializer:

    # ======= Validation cpf tests =======
    def test_duplicate_cpf_is_rejected(self, admin_user):
        CustomerFactory(cpf='52998224725')
        data = {
            'name':       'Outro Cliente',
            'cpf':        '52998224725',
            'start_date': '2024-01-01',
        }
        s = CustomerSerializer(data=data, context={'request': make_request(admin_user)})
        assert not s.is_valid()
        assert 'cpf' in s.errors

    def test_duplicated_cpf_allows_editing_same_record(self, admin_user):
        c = CustomerFactory(cpf='52998224725')
        data = {'cpf': '52998224725', 'name': 'Nome Editado'}
        s = CustomerSerializer(
            c, data=data, partial=True,
            context={'request': make_request(admin_user)},
        )
        assert s.is_valid(), s.errors


    # ======= Validation phone tests =======
    def test_duplicate_phone_is_rejected(self, admin_user):
        CustomerFactory(phone='11912345678')
        data = {'name': 'Outro Cliente', 'start_date': '2024-01-01', 'phone': '11912345678'}
        s = CustomerSerializer(data=data, context={'request': make_request(admin_user)})
        assert not s.is_valid()
        assert 'phone' in s.errors

    def test_duplicated_phone_allows_editing_same_record(self, admin_user):
        c = CustomerFactory(phone='11912345678')
        data = {'phone': '11912345678', 'name': 'Nome Editado'}
        s = CustomerSerializer(
            c, data=data, partial=True,
            context={'request': make_request(admin_user)},
        )
        assert s.is_valid(), s.errors
