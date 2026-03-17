from celery import shared_task
from django.utils import timezone
from apps.invoices.models import Invoice
from apps.notifications.models import Notification


@shared_task
def check_overdue_invoices():
    """Mark overdue invoices and create notifications."""

    today = timezone.now().date()
    overdue = Invoice.objects.filter(
        status=Invoice.Status.PENDING,
        due_date__lt=today,
    )
    for invoice in overdue:
        invoice.status = Invoice.Status.OVERDUE
        invoice.save(update_fields=["status"])

        # Create notification if not already exists
        message = f"Boleto de {invoice.customer.name} venceu em {invoice.due_date.strftime('%d/%m/%Y')} (R$ {invoice.value})"
        if not Notification.objects.filter(message=message).exists():
            Notification.objects.create(
                message=message,
                type=Notification.Type.OVERDUE,
            )
