import pytest
from apps.customers.serializers import (
    CustomerCreateUpdateSerializer,
    CustomerDetailSerializer,
    CustomerListSerializer,
)
from apps.customers.tests.factories import CustomerFactory
from apps.customers.models import Customer
from apps.invoices.tests.factories import InvoiceFactory
from apps.invoices.models import Invoice
from rest_framework.test import APIRequestFactory


def make_request(user):
    factory = APIRequestFactory()
    req = factory.post('/')
    req.user = user
    return req


@pytest.mark.django_db
class TestCustomerCreateUpdateSerializer:

    def test_valid_data_creates_customer(self, admin_user):
        data = {'name': 'João Silva', 'start_date': '2024-01-01'}
        s = CustomerCreateUpdateSerializer(data=data, context={'request': make_request(admin_user)})
        assert s.is_valid(), s.errors
        customer = s.save()
        assert customer.pk is not None
        assert customer.name == 'João Silva'
        assert customer.created_by == admin_user
        assert customer.updated_by == admin_user

    def test_missing_name_is_invalid(self, admin_user):
        data = {'start_date': '2024-01-01'}
        s = CustomerCreateUpdateSerializer(data=data, context={'request': make_request(admin_user)})
        assert not s.is_valid()
        assert 'name' in s.errors

    # ── CPF ──────────────────────────────────────────────────────────────────

    def test_duplicate_cpf_is_rejected(self, admin_user):
        CustomerFactory(cpf='52998224725')
        data = {'name': 'Outro Cliente', 'cpf': '52998224725', 'start_date': '2024-01-01'}
        s = CustomerCreateUpdateSerializer(data=data, context={'request': make_request(admin_user)})
        assert not s.is_valid()
        assert 'cpf' in s.errors

    def test_duplicate_cpf_allows_editing_same_record(self, admin_user):
        c = CustomerFactory(cpf='52998224725')
        data = {'cpf': '52998224725', 'name': 'Nome Editado'}
        s = CustomerCreateUpdateSerializer(
            c, data=data, partial=True,
            context={'request': make_request(admin_user)},
        )
        assert s.is_valid(), s.errors

    def test_invalid_cpf_is_rejected(self, admin_user):
        data = {'name': 'Cliente', 'cpf': '00000000000', 'start_date': '2024-01-01'}
        s = CustomerCreateUpdateSerializer(data=data, context={'request': make_request(admin_user)})
        assert not s.is_valid()
        assert 'cpf' in s.errors

    # ── Phone ─────────────────────────────────────────────────────────────────

    def test_duplicate_phone_is_rejected(self, admin_user):
        CustomerFactory(phone='11912345678')
        data = {'name': 'Outro Cliente', 'start_date': '2024-01-01', 'phone': '11912345678'}
        s = CustomerCreateUpdateSerializer(data=data, context={'request': make_request(admin_user)})
        assert not s.is_valid()
        assert 'phone' in s.errors

    def test_duplicate_phone_allows_editing_same_record(self, admin_user):
        c = CustomerFactory(phone='11912345678')
        data = {'phone': '11912345678', 'name': 'Nome Editado'}
        s = CustomerCreateUpdateSerializer(
            c, data=data, partial=True,
            context={'request': make_request(admin_user)},
        )
        assert s.is_valid(), s.errors

    def test_phone_is_optional(self, admin_user):
        data = {'name': 'Sem Telefone', 'start_date': '2024-01-01'}
        s = CustomerCreateUpdateSerializer(data=data, context={'request': make_request(admin_user)})
        assert s.is_valid(), s.errors

    def test_blank_phone_is_normalized_to_null(self, admin_user):
        data = {'name': 'Sem Telefone', 'start_date': '2024-01-01', 'phone': ''}
        s = CustomerCreateUpdateSerializer(data=data, context={'request': make_request(admin_user)})
        assert s.is_valid(), s.errors
        customer = s.save()
        assert customer.phone is None

    def test_multiple_customers_can_be_saved_with_blank_phone(self, admin_user):
        first = CustomerCreateUpdateSerializer(
            data={'name': 'Cliente 1', 'start_date': '2024-01-01', 'phone': ''},
            context={'request': make_request(admin_user)},
        )
        second = CustomerCreateUpdateSerializer(
            data={'name': 'Cliente 2', 'start_date': '2024-01-01', 'phone': ''},
            context={'request': make_request(admin_user)},
        )

        assert first.is_valid(), first.errors
        assert second.is_valid(), second.errors
        assert first.save().phone is None
        assert second.save().phone is None

    def test_audit_updated_by_is_set_on_update(self, admin_user, financeiro_user):
        c = CustomerFactory()
        data = {'name': 'Nome Atualizado'}
        s = CustomerCreateUpdateSerializer(
            c, data=data, partial=True,
            context={'request': make_request(financeiro_user)},
        )
        assert s.is_valid(), s.errors
        updated = s.save()
        assert updated.updated_by == financeiro_user


@pytest.mark.django_db
class TestCustomerDetailSerializer:

    def test_contains_expected_fields(self, admin_user):
        c = CustomerFactory()
        c.created_by = admin_user
        c.updated_by = admin_user
        c.save()
        s = CustomerDetailSerializer(c)
        for field in ['id', 'name', 'phone', 'cpf', 'start_date', 'birthday',
                      'observations', 'is_active', 'created_at', 'created_by',
                      'updated_at', 'updated_by']:
            assert field in s.data

    def test_created_by_shows_full_name(self, admin_user):
        c = CustomerFactory()
        c.created_by = admin_user
        c.save()
        s = CustomerDetailSerializer(c)
        assert s.data['created_by'] == admin_user.get_full_name()


@pytest.mark.django_db
class TestCustomerListSerializer:

    def test_contains_expected_fields(self):
        c = CustomerFactory()
        c.is_overdue = False
        s = CustomerListSerializer(c)
        for field in ['id', 'name', 'is_active', 'is_overdue', 'created_at']:
            assert field in s.data

    def test_is_overdue_field_is_present(self):
        from django.db.models import Exists, OuterRef
        customer = CustomerFactory()
        InvoiceFactory(customer=customer, status=Invoice.Status.OVERDUE)
        annotated = (
            Customer.objects
            .filter(pk=customer.pk)
            .annotate(is_overdue=Exists(
                Invoice.objects.filter(
                    customer=OuterRef('pk'),
                    status=Invoice.Status.OVERDUE
                )
            ))
            .get()
        )
        s = CustomerListSerializer(annotated)
        assert s.data['is_overdue'] is True
