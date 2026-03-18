import pytest
from apps.invoices.models import Invoice
from apps.customers.tests.factories import CustomerFactory

@pytest.mark.django_db
def test_invoice_str():
    customer = CustomerFactory()
    invoice = Invoice.objects.create(
        customer=customer,
        value=123.45,
        due_date="2026-04-01",
        status="PENDING"
    )
    expected = f"{customer} – 2026-04-01 - 123.45"
    assert str(invoice) == expected
