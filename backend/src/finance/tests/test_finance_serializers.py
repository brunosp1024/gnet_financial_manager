import pytest
from rest_framework.test import APIRequestFactory
from finance.serializers import (
    TransactionCreateSerializer,
    TransactionUpdateSerializer,
    TransactionListSerializer,
    TransactionDetailSerializer,
)
from finance.tests.factories import TransactionFactory
from customers.tests.factories import CustomerFactory


def make_request(user):
    f = APIRequestFactory()
    req = f.post('/')
    req.user = user
    return req


@pytest.mark.django_db
class TestTransactionSerializer:

    # ── TransactionCreateSerializer ───────────────────────────────────────────────────────
    def test_create_income_requires_payment_method(self, admin_user):
        data = {
            'type': 'INCOME',
            'category': 'MONTHLY_FEE',
            'value': '100.00',
        }
        ts = TransactionCreateSerializer(data=data, context={'request': make_request(admin_user)})
        assert not ts.is_valid()
        assert 'payment_method' in ts.errors

    def test_create_income_invalid_category(self, admin_user):
        data = {
            'type': 'INCOME',
            'category': 'LOGISTIC',
            'payment_method': 'PIX',
            'value': '50.00',
        }
        ts = TransactionCreateSerializer(data=data, context={'request': make_request(admin_user)})
        assert not ts.is_valid()
        assert 'category' in ts.errors

    def test_create_expense_invalid_category(self, admin_user):
        data = {
            'type': 'EXPENSE',
            'category': 'MONTHLY_FEE',
            'payment_method': '',
            'value': '10.00',
        }
        ts = TransactionCreateSerializer(data=data, context={'request': make_request(admin_user)})
        assert not ts.is_valid()
        assert 'category' in ts.errors

    def test_create_with_customer_id_sets_customer(self, admin_user):
        customer = CustomerFactory()
        data = {
            'type': 'INCOME',
            'category': 'MONTHLY_FEE',
            'payment_method': 'PIX',
            'customer_id': str(customer.pk),
            'value': '120.00',
        }
        ts = TransactionCreateSerializer(data=data, context={'request': make_request(admin_user)})
        assert ts.is_valid(), ts.errors
        t = ts.save()
        assert t.customer_id == customer.pk

    # ── TransactionListSerializer ───────────────────────────────────────────────────────
    def test_list_serializer_displays_fields(self):
        t = TransactionFactory()
        s = TransactionListSerializer(t)
        assert s.data['type_display'] == t.get_type_display()
        assert s.data['category_display'] == t.get_category_display()
        assert s.data['customer_name'] == t.customer.name

    # ── TransactionDetailSerializer ───────────────────────────────────────────────────────
    def test_detail_serializer_includes_user_names(self, admin_user):
        t = TransactionFactory()
        t.created_by = admin_user
        t.updated_by = admin_user
        t.save()
        s = TransactionDetailSerializer(t)
        assert s.data['created_by_name'] == admin_user.get_full_name()
        assert s.data['updated_by_name'] == admin_user.get_full_name()
        assert s.data['customer_name'] == t.customer.name

    # ── TransactionUpdateSerializer ───────────────────────────────────────────────────────
    def test_update_serializer_uses_instance_defaults(self, admin_user):
        t = TransactionFactory(type='INCOME', category='MONTHLY_FEE', payment_method='PIX')
        data = {'description': 'updated'}
        us = TransactionUpdateSerializer(instance=t, data=data, partial=True, context={'request': make_request(admin_user)})
        assert us.is_valid(), us.errors
        updated = us.save()
        assert updated.type == t.type
        assert updated.category == t.category
        assert updated.payment_method == t.payment_method
