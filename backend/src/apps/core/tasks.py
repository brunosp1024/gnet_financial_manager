import os
from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from apps.customers.models import Customer
from apps.employees.models import Employee
from apps.finance.models import Transaction
from apps.invoices.models import Invoice
from apps.users.models import User


@shared_task
def physical_delete_soft_deleted():
    """Physically delete records soft-deleted more than N days ago."""

    days = int(os.getenv("PHYSICAL_DELETE_AFTER_DAYS", 90))
    cutoff = timezone.now() - timedelta(days=days)

    for Model in [Customer, Employee, Transaction, Invoice, User]:
        deleted = Model.dm_objects.filter(
            deleted_at__isnull=False,
            deleted_at__lte=cutoff,
        )
        count = deleted.count()
        deleted.delete()
        if count:
            print(f"[Cleanup] Deleted {count} records from {Model.__name__}")
