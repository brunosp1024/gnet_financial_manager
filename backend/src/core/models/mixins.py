import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class AuditMixin(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_created',
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_updated',
    )
    
    class Meta:
        abstract = True

class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)

class SoftDeleteMixin(models.Model):
    deleted_at = models.DateTimeField('Deleted at', default=None, null=True, blank=True)

    objects = CustomManager()
    dm_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, user=None):
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def hard_delete(self, using=None, keep_parents=False):
        return super().delete(using=using, keep_parents=keep_parents)


class BaseModel(UUIDMixin, TimestampMixin, AuditMixin, SoftDeleteMixin):

    class Meta:
        abstract = True