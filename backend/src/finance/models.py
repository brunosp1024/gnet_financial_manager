# finance/models.py
from django.db import models
from django.conf import settings
from uuid import uuid4


class Transaction(models.Model):
    class Type(models.TextChoices):
        INCOME = "INCOME", "Entrada"
        EXPENSE = "EXPENSE", "Saida"

    class Category(models.TextChoices):
        MONTHLY_FEE = "MONTHLY_FEE", "Mensalidade"
        STORE_SERVICE = "STORE_SERVICE", "Loja / Serviços"
        LOGISTIC = "LOGISTIC", "Logística"
        PAYROLL = "PAYROLL", "Folha de Pagamento"

    class PaymentMethod(models.TextChoices):
        PIX = "PIX", "PIX"
        CASH = "CASH", "Dinheiro"
        CARD = "CARD", "Cartão"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    type = models.CharField(max_length=10, choices=Type.choices)
    category = models.CharField(max_length=30, choices=Category.choices)
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices, blank=True)
    description = models.CharField(max_length=300)
    value = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="transactions"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "transactions"
        ordering = ["-created_at"]
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
