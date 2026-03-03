from django.contrib.auth.models import AbstractUser
from core.models.mixins.deleted_mixin import DeletedMixin
from core.models.mixins.timestampable_mixin import TimestampableMixin


class User(AbstractUser, TimestampableMixin, DeletedMixin):
    class Meta:
        db_table = "users"
        ordering = ["-created_at"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"