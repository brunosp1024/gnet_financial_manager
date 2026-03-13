from django.db import models
from core.models.person import Person


class Customer(Person):

    class Meta:
        db_table = "customers"
        ordering = ["-created_at"]
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
