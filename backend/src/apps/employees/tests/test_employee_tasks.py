from datetime import date, timedelta
from unittest.mock import patch
import pytest
from django.utils import timezone

from apps.employees.tasks import check_employee_birthdays
from apps.employees.tests.factories import EmployeeFactory
from apps.notifications.models import Notification


@pytest.mark.django_db
class TestCheckEmployeeBirthdays:
    """Tests for check_employee_birthdays task."""

    def test_creates_notification_for_birthday_today(self):
        """Should create notification when employee has birthday today."""
        today = timezone.now().date()
        birth_date = date(1990, today.month, today.day)
        employee = EmployeeFactory(birthday=birth_date, is_active=True)

        check_employee_birthdays()

        # Notification should be created
        notification = Notification.objects.get(
            type=Notification.Type.BIRTHDAY,
            message__contains=employee.name,
        )
        assert employee.name in notification.message
        assert "🎂" in notification.message

    def test_calculates_correct_age(self):
        """Should calculate correct age in birthday notification."""
        today = timezone.now().date()
        birth_year = today.year - 25
        birth_date = date(birth_year, today.month, today.day)
        EmployeeFactory(birthday=birth_date, is_active=True)

        check_employee_birthdays()

        notification = Notification.objects.get()
        assert "25 anos" in notification.message

    def test_does_not_create_duplicate_notification(self):
        """Should not create duplicate notifications for same birthday."""
        today = timezone.now().date()
        birth_date = date(1990, today.month, today.day)
        employee = EmployeeFactory(birthday=birth_date, is_active=True)

        # Run task twice
        check_employee_birthdays()
        check_employee_birthdays()

        # Only one notification should exist
        notifications = Notification.objects.filter(
            type=Notification.Type.BIRTHDAY,
            message__contains=employee.name,
        )
        assert notifications.count() == 1

    def test_does_not_create_for_inactive_employees(self):
        """Should not create notification for inactive employees."""
        check_employee_birthdays()

        # No notification should be created
        notification_count = Notification.objects.filter(
            type=Notification.Type.BIRTHDAY,
        ).count()
        assert notification_count == 0

    def test_does_not_create_for_future_birthdays(self):
        """Should not create notification for future birthdays."""
        today = timezone.now().date()
        # Birthday tomorrow
        tomorrow = today + timedelta(days=1)
        birth_date = date(1990, tomorrow.month, tomorrow.day)
        employee = EmployeeFactory(birthday=birth_date, is_active=True)

        check_employee_birthdays()

        # No notification should be created
        notification_count = Notification.objects.filter(
            type=Notification.Type.BIRTHDAY,
            message__contains=employee.name,
        ).count()
        assert notification_count == 0

    def test_does_not_create_for_past_birthdays(self):
        """Should not create notification for past birthdays."""
        today = timezone.now().date()
        # Birthday yesterday
        yesterday = today - timedelta(days=1)
        birth_date = date(1990, yesterday.month, yesterday.day)
        employee = EmployeeFactory(birthday=birth_date, is_active=True)

        check_employee_birthdays()

        # No notification should be created
        notification_count = Notification.objects.filter(
            type=Notification.Type.BIRTHDAY,
            message__contains=employee.name,
        ).count()
        assert notification_count == 0

    def test_creates_notifications_for_multiple_birthdays(self):
        """Should create notifications for multiple employees with birthdays."""
        today = timezone.now().date()
        birth_date = date(1990, today.month, today.day)

        employee1 = EmployeeFactory(birthday=birth_date, is_active=True)
        employee2 = EmployeeFactory(birthday=birth_date, is_active=True)

        check_employee_birthdays()

        # Two notifications for active employees
        notifications = Notification.objects.filter(
            type=Notification.Type.BIRTHDAY,
        )
        assert notifications.count() == 2
        assert all(
            any(emp.name in n.message for n in notifications)
            for emp in [employee1, employee2]
        )

    def test_handles_leap_year_birthdays(self):
        """Should handle employees born on Feb 29."""
        employee = EmployeeFactory(is_active=True)
        employee.birthday = date(1992, 2, 28)
        employee.save()

        # Simulate running task on Feb 28 of a non-leap year
        with patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = timezone.datetime(2024, 2, 28)
            check_employee_birthdays()

            notification_count = Notification.objects.filter(
                type=Notification.Type.BIRTHDAY,
                message__contains=employee.name,
            ).count()
            assert notification_count == 1
        
        # Should not create notification
        with patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = timezone.datetime(2024, 3, 28)
            check_employee_birthdays()

            notification_count = Notification.objects.filter(
                type=Notification.Type.BIRTHDAY,
                message__contains=employee.name,
            ).count()
            assert notification_count == 1
