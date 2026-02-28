# emplyeess/models.py
from django.db import models
from uuid import uuid4


class Employee(models.Model):
    class Modality(models.TextChoices):
        CLT = "CLT", "CLT"
        SERVICE_PROVIDER = "SERVICE_PROVIDER", "Prestador de Serviços"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=100, blank=True)
    cpf = models.CharField(max_length=14, unique=True)
    address = models.TextField(blank=True)
    start_date = models.DateField()
    birthday = models.DateField()
    modality = models.CharField(max_length=20, choices=Modality.choices, default=Modality.CLT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "employees"
        ordering = ["-created_at"]
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
