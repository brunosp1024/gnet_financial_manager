from datetime import timedelta
import pytest
from django.utils import timezone

from apps.notifications.tasks import delete_old_notifications
from apps.notifications.tests.factories import NotificationFactory


@pytest.mark.django_db
class TestDeleteOldNotifications:
    """Tests for delete_old_notifications task."""

    def test_deletes_notifications_older_than_cutoff(self):
        """Should delete notifications older than 30 days."""
        # Create old notification (40 days ago)
        old_date = timezone.now() - timedelta(days=40)
        old_notification = NotificationFactory()
        old_notification.created_at = old_date
        old_notification.save(update_fields=["created_at"])

        # Create recent notification (10 days ago)
        recent_date = timezone.now() - timedelta(days=10)
        recent_notification = NotificationFactory()
        recent_notification.created_at = recent_date
        recent_notification.save(update_fields=["created_at"])

        # Execute task
        delete_old_notifications()

        # Old notification should be deleted
        assert not NotificationFactory._meta.model.objects.filter(
            pk=old_notification.pk
        ).exists()
        # Recent notification should remain
        assert NotificationFactory._meta.model.objects.filter(
            pk=recent_notification.pk
        ).exists()

    def test_respects_retention_days_env(self, monkeypatch):
        """Should respect NOTIFICATION_RETENTION_DAYS env variable."""
        # Create notification 30 days ago
        old_date = timezone.now() - timedelta(days=30)
        notification = NotificationFactory()
        notification.created_at = old_date
        notification.save(update_fields=["created_at"])

        # Run with default 30 days
        delete_old_notifications()
        # Should be deleted (equal to cutoff)
        assert not NotificationFactory._meta.model.objects.filter(
            pk=notification.pk
        ).exists()

    def test_respects_custom_retention_days_env(self, monkeypatch):
        """Should use custom retention days from environment."""
        # Create notification 15 days ago
        old_date = timezone.now() - timedelta(days=15)
        notification = NotificationFactory()
        notification.created_at = old_date
        notification.save(update_fields=["created_at"])

        # Default 30 days: should not delete
        delete_old_notifications()
        assert NotificationFactory._meta.model.objects.filter(
            pk=notification.pk
        ).exists()

        # Change to 10 days cutoff
        monkeypatch.setenv('NOTIFICATION_RETENTION_DAYS', '10')
        delete_old_notifications()

        # Now should be deleted
        assert not NotificationFactory._meta.model.objects.filter(
            pk=notification.pk
        ).exists()

    def test_handles_empty_queryset(self):
        """Should handle case with no old notifications gracefully."""
        # Create only recent notifications
        for _ in range(3):
            notification = NotificationFactory()
            notification.created_at = timezone.now() - timedelta(days=5)
            notification.save(update_fields=["created_at"])

        count_before = NotificationFactory._meta.model.objects.count()
        delete_old_notifications()
        count_after = NotificationFactory._meta.model.objects.count()

        # All should remain
        assert count_before == count_after == 3

    def test_bulk_delete_multiple_old_notifications(self):
        """Should delete multiple old notifications in one operation."""
        old_date = timezone.now() - timedelta(days=40)
        for _ in range(5):
            notification = NotificationFactory()
            notification.created_at = old_date
            notification.save(update_fields=["created_at"])

        assert NotificationFactory._meta.model.objects.count() == 5
        delete_old_notifications()

        # All should be deleted
        assert NotificationFactory._meta.model.objects.count() == 0
