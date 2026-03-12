from django.db import models
from core.models.mixins.deleted_mixin import DeletedMixin
from core.models.mixins.timestampable_mixin import TimestampableMixin


class Invoice(TimestampableMixin, DeletedMixin):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendente"
        PAID = "PAID", "Pago"
        OVERDUE = "OVERDUE", "Atrasado"

    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.CASCADE,
        related_name="invoices",
    )
    value = models.DecimalField(max_digits=12, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    paid_at = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "invoices"
        ordering = ["-created_at"]
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

    def __str__(self):
        return f"{self.customer} – {self.due_date} - {self.value}"
