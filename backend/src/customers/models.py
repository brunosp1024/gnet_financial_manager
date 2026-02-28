# customers/models.py
from django.db import models
from django.conf import settings
from uuid import uuid4


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    start_date = models.DateField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="customers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "customers"
        ordering = ["-created_at"]
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
