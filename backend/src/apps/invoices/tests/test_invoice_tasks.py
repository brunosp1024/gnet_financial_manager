from datetime import timedelta
import pytest
from django.utils import timezone

from apps.invoices.tasks import check_overdue_invoices
from apps.invoices.tests.factories import InvoiceFactory
from apps.customers.tests.factories import CustomerFactory
from apps.notifications.models import Notification


@pytest.mark.django_db
class TestCheckOverdueInvoices:
    """Tests for check_overdue_invoices task."""

    def test_marks_pending_overdue_invoice_as_overdue(self):
        """Should mark pending invoices with past due date as overdue."""
        today = timezone.now().date()
        due_date = today - timedelta(days=5)
        invoice = InvoiceFactory(
            status='PENDING',
            due_date=due_date,
        )

        check_overdue_invoices()

        # Invoice should be marked as overdue
        invoice.refresh_from_db()
        assert invoice.status == 'OVERDUE'

    def test_creates_notification_for_overdue_invoice(self):
        """Should create notification when invoice becomes overdue."""
        today = timezone.now().date()
        due_date = today - timedelta(days=5)
        customer = CustomerFactory()
        invoice = InvoiceFactory(
            status='PENDING',
            due_date=due_date,
            customer=customer,
        )

        check_overdue_invoices()

        # Notification should be created
        notification = Notification.objects.filter(
            type=Notification.Type.OVERDUE,
        ).first()
        assert notification is not None
        assert customer.name in notification.message
        assert invoice.due_date.strftime('%d/%m/%Y') in notification.message

    def test_notification_includes_invoice_value(self):
        """Should include invoice value in notification."""
        today = timezone.now().date()
        due_date = today - timedelta(days=5)
        customer = CustomerFactory()
        InvoiceFactory(
            status='PENDING',
            due_date=due_date,
            customer=customer,
            value=1500.00,
        )

        check_overdue_invoices()

        notification = Notification.objects.filter(type=Notification.Type.OVERDUE).first()
        assert 'R$ 1500' in notification.message

    def test_does_not_mark_pending_invoice_with_future_due_date(self):
        """Should not mark pending invoices with future due date as overdue."""
        today = timezone.now().date()
        due_date = today + timedelta(days=10)
        invoice = InvoiceFactory(
            status='PENDING',
            due_date=due_date,
        )

        check_overdue_invoices()

        # Invoice should remain PENDING
        invoice.refresh_from_db()
        assert invoice.status == 'PENDING'

    def test_does_not_create_notification_twice(self):
        """Should not create duplicate notifications for same overdue invoice."""
        today = timezone.now().date()
        due_date = today - timedelta(days=5)
        customer = CustomerFactory()
        InvoiceFactory(
            status='PENDING',
            due_date=due_date,
            customer=customer,
        )

        # Run task twice
        check_overdue_invoices()
        check_overdue_invoices()

        # Only one notification should exist
        notifications = Notification.objects.filter(
            type=Notification.Type.OVERDUE,
            message__contains=customer.name,
        )
        assert notifications.count() == 1

    def test_does_not_process_already_overdue_invoices_again(self):
        """Should handle invoices already marked as overdue gracefully."""
        today = timezone.now().date()
        due_date = today - timedelta(days=5)
        customer = CustomerFactory()
        InvoiceFactory(
            status='OVERDUE',  # Already overdue
            due_date=due_date,
            customer=customer,
        )

        check_overdue_invoices()

        # Task should not process already overdue invoices
        invoices_processed = InvoiceFactory._meta.model.objects.filter(
            status='OVERDUE',
            due_date__lt=today,
        ).count()
        assert invoices_processed == 1

    def test_processes_multiple_overdue_invoices(self):
        """Should process multiple overdue invoices in one run."""
        today = timezone.now().date()
        due_date = today - timedelta(days=5)

        customers = [CustomerFactory() for _ in range(3)]
        [
            InvoiceFactory(
                status='PENDING',
                due_date=due_date,
                customer=customers[i],
            )
            for i in range(3)
        ]

        check_overdue_invoices()

        # All invoices should be marked as overdue
        overdue_count = InvoiceFactory._meta.model.objects.filter(
            status='OVERDUE',
        ).count()
        assert overdue_count == 3

        # All notifications should be created
        notifications = Notification.objects.filter(
            type=Notification.Type.OVERDUE,
        ).count()
        assert notifications == 3

    def test_ignores_paid_or_already_overdue_invoices(self):
        """Should only process PENDING invoices."""
        today = timezone.now().date()
        due_date = today - timedelta(days=5)

        # Create invoices with different statuses
        pending = InvoiceFactory(status='PENDING', due_date=due_date)
        paid = InvoiceFactory(status='PAID', due_date=due_date)
        already_overdue = InvoiceFactory(status='OVERDUE', due_date=due_date)

        check_overdue_invoices()

        # Only PENDING should be processed
        pending.refresh_from_db()
        paid.refresh_from_db()
        already_overdue.refresh_from_db()

        assert pending.status == 'OVERDUE'
        assert paid.status == 'PAID'
        assert already_overdue.status == 'OVERDUE'
