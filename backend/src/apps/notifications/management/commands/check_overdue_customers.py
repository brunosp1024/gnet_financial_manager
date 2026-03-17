from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.customers.models import Customer
from apps.notifications.models import Notification

OVERDUE_DAYS = 7


class Command(BaseCommand):
    help = "Cria notificações para clientes com faturas em atraso há mais de 7 dias."

    def handle(self, *args, **kwargs):
        # TODO: quando o modelo Invoice existir, substituir este filtro por:
        #
        #   from apps.finance.models import Invoice
        #   cutoff = timezone.now().date() - timezone.timedelta(days=OVERDUE_DAYS)
        #   overdue_customer_ids = (
        #       Invoice.objects
        #       .filter(due_date__lte=cutoff, paid=False)
        #       .values_list("customer_id", flat=True)
        #       .distinct()
        #   )
        #   customers = Customer.objects.filter(id__in=overdue_customer_ids, is_active=True)
        #
        # Por enquanto, usa o campo is_overdue como proxy.
        customers = Customer.objects.filter(is_overdue=True, is_active=True)

        today = timezone.now().date()
        created_count = 0

        for customer in customers:
            already_notified = customer.notifications.filter(
                type=Notification.Type.OVERDUE,
                created_at__date=today,
            ).exists()

            if not already_notified:
                Notification.objects.create(
                    customer=customer,
                    type=Notification.Type.OVERDUE,
                    message=f"O cliente {customer.name} possui fatura(s) em atraso há mais de {OVERDUE_DAYS} dias.",
                )
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"{created_count} notificação(ões) criada(s).")
        )
