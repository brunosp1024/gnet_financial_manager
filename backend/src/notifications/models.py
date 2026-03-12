from uuid import uuid4
from django.db import models


class Notification(models.Model):
    class Type(models.TextChoices):
        OVERDUE = "OVERDUE", "Fatura em Atraso"
        NEW_CUSTOMER = "NEW_CUSTOMER", "Novo Cliente"
        BIRTHDAY = "BIRTHDAY", "Aniversário do Funcionário"
        ANOTHER = "ANOTHER", "Notificação"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    type = models.CharField(max_length=30, choices=Type.choices, default=Type.ANOTHER)
    message = models.CharField(max_length=500)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notifications"
        ordering = ["-created_at"]
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
