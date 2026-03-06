from django.db import models
from .mixins.deleted_mixin import DeletedMixin
from .mixins.timestampable_mixin import TimestampableMixin
from utils.validators import validate_cpf, validate_phone


class Person(TimestampableMixin, DeletedMixin):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True, unique=True, validators=[validate_phone])
    cpf = models.CharField(max_length=11, blank=True, validators=[validate_cpf])
    start_date = models.DateField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    observations = models.TextField(blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name