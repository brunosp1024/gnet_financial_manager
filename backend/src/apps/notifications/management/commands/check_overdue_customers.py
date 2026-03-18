import os
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.invoices.models import Invoice
from apps.notifications.models import Notification


class Command(BaseCommand):
    help = "Cria notificações para clientes com faturas em atraso há mais de 7 dias."

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        overdue_days = int(os.getenv('OVERDUE_DAYS', 7))
        cutoff = today - timezone.timedelta(days=overdue_days)
        created_count = 0

        overdue_invoices = Invoice.objects.filter(
            status=Invoice.Status.OVERDUE,
            due_date__lte=cutoff,
            customer__is_active=True,
        ).select_related("customer")

        for invoice in overdue_invoices:
            current_overdue_days = (today - invoice.due_date).days
            message = (
                f"O cliente {invoice.customer.name} possui fatura em atraso "
                f"desde {invoice.due_date.strftime('%d/%m/%Y')} (há {current_overdue_days} dias)."
            )
            already_notified = Notification.objects.filter(
                type=Notification.Type.OVERDUE,
                message=message,
            ).exists()
            very_overdue = current_overdue_days > overdue_days
            if not already_notified or (very_overdue and current_overdue_days % overdue_days == 0):
                Notification.objects.create(
                    type=Notification.Type.OVERDUE,
                    message=message,
                )
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"{created_count} notificação(ões) criada(s).")
        )
