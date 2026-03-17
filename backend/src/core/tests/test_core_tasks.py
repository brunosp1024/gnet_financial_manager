import os
from datetime import timedelta
import pytest
from django.utils import timezone
from django.test import override_settings

from core.tasks import physical_delete_soft_deleted
from customers.tests.factories import CustomerFactory
from employees.tests.factories import EmployeeFactory
from invoices.tests.factories import InvoiceFactory
from finance.tests.factories import TransactionFactory
from users.tests.factories import UserFactory


@pytest.mark.django_db
class TestPhysicalDeleteSoftDeleted:
    """Tests for physical_delete_soft_deleted task."""

    def test_deletes_soft_deleted_older_than_cutoff(self):
        """Should physically delete records older than cutoff date."""
        # Create old soft-deleted customer (100 days ago)
        old_date = timezone.now() - timedelta(days=100)
        customer = CustomerFactory()
        customer.deleted_at = old_date
        customer.save()

        # Create recent soft-deleted customer (30 days ago)
        recent_date = timezone.now() - timedelta(days=30)
        recent_customer = CustomerFactory()
        recent_customer.deleted_at = recent_date
        recent_customer.save()

        # Execute task with default 90 days cutoff
        physical_delete_soft_deleted()

        # Old record should be deleted
        assert not CustomerFactory._meta.model.dm_objects.filter(pk=customer.pk).exists()
        # Recent record should remain
        assert CustomerFactory._meta.model.dm_objects.filter(pk=recent_customer.pk).exists()

    def test_deletes_all_models(self):
        """Should delete soft-deleted records from all models."""
        old_date = timezone.now() - timedelta(days=100)

        # Create old soft-deleted records in all models
        customer = CustomerFactory()
        customer.deleted_at = old_date
        customer.save()

        employee = EmployeeFactory()
        employee.deleted_at = old_date
        employee.save()

        invoice = InvoiceFactory()
        invoice.deleted_at = old_date
        invoice.save()

        transaction = TransactionFactory()
        transaction.deleted_at = old_date
        transaction.save()

        user = UserFactory()
        user.deleted_at = old_date
        user.save()

        # Execute task
        physical_delete_soft_deleted()

        # All soft-deleted records should be removed
        assert not CustomerFactory._meta.model.dm_objects.filter(pk=customer.pk).exists()
        assert not EmployeeFactory._meta.model.dm_objects.filter(pk=employee.pk).exists()
        assert not InvoiceFactory._meta.model.dm_objects.filter(pk=invoice.pk).exists()
        assert not TransactionFactory._meta.model.dm_objects.filter(pk=transaction.pk).exists()
        assert not UserFactory._meta.model.dm_objects.filter(pk=user.pk).exists()

    def test_respects_custom_cutoff_days(self):
        """Should respect PHYSICAL_DELETE_AFTER_DAYS environment variable."""
        # Create soft-deleted record 60 days ago
        old_date = timezone.now() - timedelta(days=60)
        customer = CustomerFactory()
        customer.deleted_at = old_date
        customer.save()

        # Run with 90 days cutoff (default)
        physical_delete_soft_deleted()
        # Should not be deleted yet
        assert CustomerFactory._meta.model.dm_objects.filter(pk=customer.pk).exists()

        # Run with 30 days cutoff
        with override_settings(
            CELERY_BEAT_SCHEDULE={
                'test': {'task': 'core.tasks.physical_delete_soft_deleted', 'schedule': None}
            }
        ):
            with pytest.MonkeyPatch.context() as mp:
                mp.setenv('PHYSICAL_DELETE_AFTER_DAYS', '30')
                physical_delete_soft_deleted()

        # Now should be deleted
        assert not CustomerFactory._meta.model.dm_objects.filter(pk=customer.pk).exists()

    def test_does_not_delete_non_soft_deleted(self):
        """Should not delete records that aren't soft-deleted."""
        customer = CustomerFactory()  # No deleted_at
        original_count = CustomerFactory._meta.model.objects.count()

        physical_delete_soft_deleted()

        # Record should still exist
        assert CustomerFactory._meta.model.objects.filter(pk=customer.pk).exists()
        assert CustomerFactory._meta.model.objects.count() == original_count

    def test_does_not_delete_recent_soft_deleted(self):
        """Should not delete recently soft-deleted records."""
        recent_date = timezone.now() - timedelta(days=10)
        customer = CustomerFactory()
        customer.deleted_at = recent_date
        customer.save()

        physical_delete_soft_deleted()

        # Recent soft-deleted record should remain
        assert CustomerFactory._meta.model.dm_objects.filter(pk=customer.pk).exists()
