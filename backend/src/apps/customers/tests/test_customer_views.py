import pytest
from apps.customers.models import Customer
from apps.customers.tests.factories import CustomerFactory
from apps.invoices.tests.factories import InvoiceFactory
from apps.invoices.models import Invoice

LIST_URL = '/api/customers/'


def DETAIL_URL(pk):
    return f'/api/customers/{pk}/'


@pytest.mark.django_db
class TestCustomerAuthentication:

    def test_unauthenticated_returns_401(self, api_client):
        assert api_client.get(LIST_URL).status_code == 401

    def test_no_group_returns_403(self, no_group_client):
        assert no_group_client.get(LIST_URL).status_code == 403


@pytest.mark.django_db
class TestCustomerCRUD:

    def test_create_sets_default_is_active(self, admin_client):
        data = {'name': 'New Customer', 'start_date': '2024-01-01'}
        res = admin_client.post(LIST_URL, data, format='json')
        assert res.status_code == 201
        assert Customer.objects.get(pk=res.data['id']).is_active is True

    def test_retrieve_uses_detail_serializer(self, admin_client):
        c = CustomerFactory()
        res = admin_client.get(DETAIL_URL(c.pk))
        assert res.status_code == 200
        for field in ['id', 'name', 'created_at', 'updated_at', 'created_by', 'updated_by']:
            assert field in res.data

    def test_list_uses_list_serializer(self, admin_client):
        CustomerFactory()
        res = admin_client.get(LIST_URL)
        assert res.status_code == 200
        assert 'is_overdue' in res.data['results'][0]

    def test_partial_update_changes_field(self, admin_client):
        c = CustomerFactory(name='Old Name')
        res = admin_client.patch(DETAIL_URL(c.pk), {'name': 'New Name'})
        assert res.status_code == 200
        c.refresh_from_db()
        assert c.name == 'New Name'

    def test_create_missing_name_returns_400(self, admin_client):
        res = admin_client.post(LIST_URL, {'start_date': '2024-01-01'})
        assert res.status_code == 400
        assert 'name' in res.data


@pytest.mark.django_db
class TestCustomerFilters:

    def test_search_by_name(self, admin_client):
        CustomerFactory(name='Zacarias Provider')
        CustomerFactory(name='Maria Customer')
        res = admin_client.get(LIST_URL, {'search': 'Zacarias'})
        assert res.status_code == 200
        assert res.data['count'] == 1

    def test_search_by_cpf(self, admin_client):
        CustomerFactory(cpf='52998224725')
        CustomerFactory(cpf='')
        res = admin_client.get(LIST_URL, {'search': '529'})
        assert res.status_code == 200
        assert res.data['count'] == 1

    def test_filter_by_is_active(self, admin_client):
        CustomerFactory(is_active=True)
        CustomerFactory(is_active=False)
        res = admin_client.get(LIST_URL, {'is_active': 'true'})
        assert res.status_code == 200
        assert res.data['count'] == 1

    def test_filter_by_address(self, admin_client):
        CustomerFactory(address='123 Main St')
        CustomerFactory(address='456 Elm St')
        res = admin_client.get(LIST_URL, {'address': '123'})
        assert res.status_code == 200
        assert res.data['count'] == 1

    def test_filter_by_is_overdue_true(self, admin_client):
        overdue_customer = CustomerFactory()
        InvoiceFactory(customer=overdue_customer, status=Invoice.Status.OVERDUE)
        CustomerFactory()  # sem fatura em atraso
        res = admin_client.get(LIST_URL, {'is_overdue': 'true'})
        assert res.status_code == 200
        assert res.data['count'] == 1
        assert str(res.data['results'][0]['id']) == str(overdue_customer.pk)

    def test_filter_by_is_overdue_false(self, admin_client):
        overdue_customer = CustomerFactory()
        InvoiceFactory(customer=overdue_customer, status=Invoice.Status.OVERDUE)
        CustomerFactory()  # sem fatura em atraso
        res = admin_client.get(LIST_URL, {'is_overdue': 'false'})
        assert res.status_code == 200
        assert res.data['count'] == 1
        assert str(res.data['results'][0]['id']) != str(overdue_customer.pk)

    def test_is_overdue_appears_in_list_response(self, admin_client):
        customer = CustomerFactory()
        InvoiceFactory(customer=customer, status=Invoice.Status.OVERDUE)
        res = admin_client.get(LIST_URL)
        assert res.status_code == 200
        result = next(r for r in res.data['results'] if str(r['id']) == str(customer.pk))
        assert result['is_overdue'] is True
