import pytest
from datetime import date, timedelta
from django.utils import timezone
from invoices.models import Invoice
from invoices.tests.factories import InvoiceFactory
from customers.tests.factories import CustomerFactory

LIST_URL = '/api/invoices/'

def DETAIL_URL(pk):
    return f'/api/invoices/{pk}/'


# ── Authentication ────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestInvoiceAuthentication:

    def test_unauthenticated_returns_401(self, api_client):
        assert api_client.get(LIST_URL).status_code == 401

    def test_unauthenticated_create_returns_401(self, api_client):
        assert api_client.post(LIST_URL, {}).status_code == 401


# ── CRUD ──────────────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestInvoiceCRUD:

    def test_create_sets_default_status_pending(self, admin_client):
        customer = CustomerFactory()
        data = {
            'customer_id': str(customer.pk),
            'value': '300.00',
            'due_date': '2026-07-01',
        }
        response = admin_client.post(LIST_URL, data)
        assert response.status_code == 201
        invoice = Invoice.objects.get(pk=response.data['id'])
        assert invoice.status == Invoice.Status.PENDING

    def test_list_returns_all_invoices(self, admin_client):
        InvoiceFactory.create_batch(4)
        response = admin_client.get(LIST_URL)
        assert response.status_code == 200
        assert response.data['count'] == 4

    def test_partial_update_changes_status(self, admin_client):
        invoice = InvoiceFactory(status='PENDING')
        response = admin_client.patch(DETAIL_URL(invoice.pk), {'status': 'PAID'})
        assert response.status_code == 200
        invoice.refresh_from_db()
        assert invoice.status == 'PAID'

    def test_partial_update_to_paid_auto_fills_paid_at(self, admin_client):
        invoice = InvoiceFactory(status='PENDING', paid_at=None)
        response = admin_client.patch(DETAIL_URL(invoice.pk), {'status': 'PAID'})
        assert response.status_code == 200
        invoice.refresh_from_db()
        assert invoice.paid_at == timezone.localdate()

    def test_delete_invoice(self, admin_client):
        invoice = InvoiceFactory()
        pk = invoice.pk
        response = admin_client.delete(DETAIL_URL(pk))
        assert response.status_code == 204
        assert not Invoice.objects.filter(pk=pk).exists()


