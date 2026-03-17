from django.contrib.auth.models import AbstractUser, UserManager
from apps.core.models.mixins import BaseModel


class ActiveUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class User(AbstractUser, BaseModel):

    objects = ActiveUserManager()
    dm_objects = UserManager()

    class Meta:
        db_table = "users"
        ordering = ["-created_at"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"