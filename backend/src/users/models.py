from django.contrib.auth.models import AbstractUser
from core.models.mixins.deleted_mixin import CustomManager, DeletedMixin
from core.models.mixins.timestampable_mixin import TimestampableMixin
from django.db import models


class User(AbstractUser, TimestampableMixin, DeletedMixin):

    objects = CustomManager()
    dm_objects = models.Manager()

    class Meta:
        db_table = "users"
        ordering = ["-created_at"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"