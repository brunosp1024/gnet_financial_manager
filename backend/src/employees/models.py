from django.db import models
from core.models.person import Person


class Employee(Person):
    class Modality(models.TextChoices):
        CLT = "CLT", "CLT"
        SERVICE_PROVIDER = "SERVICE_PROVIDER", "Prestador de Serviços"

    position = models.CharField(max_length=100, blank=True)
    modality = models.CharField(max_length=20, choices=Modality.choices, default=Modality.CLT)

    class Meta:
        db_table = "employees"
        ordering = ["-created_at"]
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
