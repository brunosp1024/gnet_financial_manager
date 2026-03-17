import os
from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from apps.notifications.models import Notification


@shared_task
def delete_old_notifications():
    """Delete old notifications."""
    days = int(os.getenv("NOTIFICATION_RETENTION_DAYS", 30))
    cutoff = timezone.now() - timedelta(days=days)
    deleted = Notification.objects.filter(created_at__lte=cutoff).delete()
    if deleted[0]:
        print(f"[Cleanup] Deleted {deleted[0]} old notifications")
