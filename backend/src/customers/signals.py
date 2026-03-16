from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.models import Notification
from .models import Customer


@receiver(post_save, sender=Customer)
def customer_created_notification(sender, instance, created, **kwargs):
    if created and not instance.deleted_at:
        Notification.objects.create(
            message=f"Novo cliente cadastrado: {instance.name}",
            type=Notification.Type.NEW_CUSTOMER,
        )
