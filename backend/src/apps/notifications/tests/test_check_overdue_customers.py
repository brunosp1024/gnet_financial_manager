import os
from datetime import timedelta
import pytest
from django.core.management import call_command
from django.utils import timezone
from apps.invoices.tests.factories import InvoiceFactory
from apps.customers.tests.factories import CustomerFactory
from apps.notifications.models import Notification


@pytest.mark.django_db
def test_management_command_creates_overdue_notification():
    today = timezone.now().date()
    customer = CustomerFactory(is_active=True)
    overdue_days = int(os.getenv('OVERDUE_DAYS', 7))
    overdue_date = today - timedelta(days=overdue_days)
    invoice = InvoiceFactory(
        customer=customer,
        status='OVERDUE',
        due_date=overdue_date,
    )
    assert Notification.objects.filter(type=Notification.Type.OVERDUE).count() == 0
    call_command('check_overdue_customers')
    notifications = Notification.objects.filter(type=Notification.Type.OVERDUE)
    assert notifications.count() == 1
    assert customer.name in notifications.first().message
    assert invoice.due_date.strftime('%d/%m/%Y') in notifications.first().message

@pytest.mark.django_db
def test_management_command_multiple_notifications():
    today = timezone.now().date()
    customer = CustomerFactory(is_active=True)
    overdue_days = int(os.getenv('OVERDUE_DAYS', 7))
    # Create invoice with overdue_days overdue
    overdue_date = today - timedelta(days=overdue_days)
    invoice = InvoiceFactory(
        customer=customer,
        status='OVERDUE',
        due_date=overdue_date,
    )
    call_command('check_overdue_customers')
    notifications = Notification.objects.filter(type=Notification.Type.OVERDUE)
    assert notifications.count() == 1
    # Run again to ensure it doesn't duplicate
    call_command('check_overdue_customers')
    assert notifications.count() == 1

@pytest.mark.django_db
def test_management_command_recreates_notification_after_overdue_period():
    today = timezone.now().date()
    customer = CustomerFactory()
    overdue_days = int(os.getenv('OVERDUE_DAYS', 7))
    # Create invoice with overdue_days overdue
    overdue_date = today - timedelta(days=overdue_days)
    invoice = InvoiceFactory(
        customer=customer,
        status='OVERDUE',
        due_date=overdue_date,
    )
    call_command('check_overdue_customers')
    notifications = Notification.objects.filter(type=Notification.Type.OVERDUE)
    assert notifications.count() == 1
    # Simulate passage of time to trigger new notification after another overdue_days
    overdue_date = overdue_date - timedelta(days=overdue_days)
    invoice = InvoiceFactory(
        customer=customer,
        status='OVERDUE',
        due_date=overdue_date,
    )
    call_command('check_overdue_customers')
    assert notifications.count() == 2

@pytest.mark.django_db
def test_management_command_no_notification_for_recent_invoice():
    today = timezone.now().date()
    customer = CustomerFactory(is_active=True)
    # Create invoice with 3 days overdue
    overdue_date = today - timedelta(days=3)
    invoice = InvoiceFactory(
        customer=customer,
        status='OVERDUE',
        due_date=overdue_date,
    )
    call_command('check_overdue_customers')
    notifications = Notification.objects.filter(type=Notification.Type.OVERDUE)
    assert notifications.count() == 0
