from django.db import models
from django.utils import timezone


class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)


class DeletedMixin(models.Model):
    deleted_at = models.DateTimeField('Deleted at', default=None, null=True, blank=True)

    objects = CustomManager()
    dm_objects = models.Manager()

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])

    def hard_delete(self, using=None, keep_parents=False):
        return super().delete(using=using, keep_parents=keep_parents)

    class Meta:
        abstract = True