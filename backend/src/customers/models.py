from django.db import models
from core.models.person import Person


class Customer(Person):
    due_date = models.DateField(blank=True, null=True)
    is_overdue = models.BooleanField(default=False)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = "customers"
        ordering = ["-created_at"]
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
