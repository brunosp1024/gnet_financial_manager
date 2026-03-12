import pytest
from datetime import date
from django.utils import timezone
from rest_framework.test import APIRequestFactory

from invoices.serializers import (
    InvoiceCreateSerializer,
    InvoiceUpdateSerializer,
    InvoiceListSerializer,
)
from invoices.tests.factories import InvoiceFactory
from customers.tests.factories import CustomerFactory


def make_request(user):
    f = APIRequestFactory()
    req = f.post('/')
    req.user = user
    return req


@pytest.mark.django_db
class TestInvoiceCreateSerializer:

    def test_valid_data_creates_invoice(self, admin_user):
        customer = CustomerFactory()
        data = {
            'customer_id': str(customer.pk),
            'value': '150.00',
            'due_date': '2026-04-01',
        }
        s = InvoiceCreateSerializer(data=data, context={'request': make_request(admin_user)})
        assert s.is_valid(), s.errors
        invoice = s.save()
        assert invoice.customer_id == customer.pk
        assert str(invoice.value) == '150.00'
        assert invoice.due_date == date(2026, 4, 1)
        assert invoice.status == 'PENDING'
        assert invoice.paid_at is None

    def test_audit_fields_are_set_on_create(self, admin_user):
        customer = CustomerFactory()
        data = {
            'customer_id': str(customer.pk),
            'value': '200.00',
            'due_date': '2026-05-01',
        }
        s = InvoiceCreateSerializer(data=data, context={'request': make_request(admin_user)})
        assert s.is_valid(), s.errors
        invoice = s.save()
        assert invoice.created_by == admin_user
        assert invoice.updated_by == admin_user


@pytest.mark.django_db
class TestInvoiceUpdateSerializer:

    def test_partial_update_preserves_status_when_omitted(self, admin_user):
        invoice = InvoiceFactory(status='PAID', paid_at=date(2026, 3, 1))
        data = {'value': '999.00'}
        s = InvoiceUpdateSerializer(
            instance=invoice, data=data, partial=True,
            context={'request': make_request(admin_user)},
        )
        assert s.is_valid(), s.errors
        updated = s.save()
        assert updated.status == 'PAID'

    def test_status_paid_auto_fills_paid_at(self, admin_user):
        invoice = InvoiceFactory(status='PENDING', paid_at=None)
        data = {'status': 'PAID'}
        s = InvoiceUpdateSerializer(
            instance=invoice, data=data, partial=True,
            context={'request': make_request(admin_user)},
        )
        assert s.is_valid(), s.errors
        updated = s.save()
        assert updated.status == 'PAID'
        assert updated.paid_at == timezone.localdate()

    def test_audit_updated_by_is_set_on_update(self, financeiro_user):
        invoice = InvoiceFactory()
        data = {'value': '300.00'}
        s = InvoiceUpdateSerializer(
            instance=invoice, data=data, partial=True,
            context={'request': make_request(financeiro_user)},
        )
        assert s.is_valid(), s.errors
        updated = s.save()
        assert updated.updated_by == financeiro_user


@pytest.mark.django_db
class TestInvoiceListSerializer:

    def test_displays_expected_fields(self):
        invoice = InvoiceFactory(status='PENDING')
        srl = InvoiceListSerializer(invoice)
        assert srl.data['customer_name'] == invoice.customer.name
        assert srl.data['status_display'] == invoice.get_status_display()
        assert str(srl.data['value']) == str(invoice.value)
        assert srl.data['due_date'] == str(invoice.due_date)
        assert srl.data['paid_at'] == None
