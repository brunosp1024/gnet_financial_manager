from celery import shared_task
from django.utils import timezone
from apps.employees.models import Employee
from apps.notifications.models import Notification


@shared_task
def check_employee_birthdays():
    """Create notifications for employee birthdays today."""

    today = timezone.now().date()
    employees = Employee.objects.filter(
        birthday__month=today.month,
        birthday__day=today.day,
        is_active=True,
    )
    for emp in employees:
        years = today.year - emp.birthday.year
        desc = f"🎂 Aniversário de {emp.name} hoje! ({years} anos)"
        if not Notification.objects.filter(
            message=desc,
            created_at__date=today,
        ).exists():
            Notification.objects.create(
                message=desc,
                type=Notification.Type.BIRTHDAY
            )
