from django.db import models
from core.models.mixins.deleted_mixin import DeletedMixin
from core.models.mixins.timestampable_mixin import TimestampableMixin


class Transaction(TimestampableMixin, DeletedMixin):
    class Type(models.TextChoices):
        INCOME = "INCOME", "Entrada"
        EXPENSE = "EXPENSE", "Saida"

    class Category(models.TextChoices):
        MONTHLY_FEE = "MONTHLY_FEE", "Mensalidade"
        STORE_SERVICE = "STORE_SERVICE", "Loja / Serviços"
        LOGISTIC = "LOGISTIC", "Logística"
        PAYROLL = "PAYROLL", "Folha de Pagamento"

    class PaymentMethod(models.TextChoices):
        CASH = "CASH", "Dinheiro"
        PIX = "PIX", "PIX"
        CARD = "CARD", "Cartão"

    type = models.CharField(max_length=10, choices=Type.choices)
    category = models.CharField(max_length=30, choices=Category.choices)
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices, blank=True)
    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions"
    )
    description = models.CharField(max_length=300, blank=True, default="")
    value = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = "transactions"
        ordering = ["-created_at"]
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
