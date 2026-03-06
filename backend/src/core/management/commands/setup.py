import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from customers.models import Customer
from employees.models import Employee
from finance.models import Transaction
from users.models import User


GROUPS = {
    'ADMIN': {
        User: ['view', 'add', 'change', 'delete'],
        Customer: ['view', 'add', 'change', 'delete'],
        Employee: ['view', 'add', 'change', 'delete'],
        Transaction: ['view', 'add', 'change', 'delete'],
    },
    'GERENTE': {
        User: ['view', 'add', 'change', 'delete'],
        Customer: ['view', 'add', 'change', 'delete'],
        Employee: ['view', 'add', 'change', 'delete'],
        Transaction: ['view', 'add', 'change', 'delete'],
    },
    'FINANCEIRO': {
        User: ['view'],
        Customer: ['view', 'add', 'change', 'delete'],
        Employee: ['view'],
        Transaction: ['view', 'add', 'change', 'delete'],
    },
}


class Command(BaseCommand):
    help = 'Create/update groups with permissions and ensure initial superuser'

    def _ensure_superuser(self):
        user_model = get_user_model()

        username = os.getenv('SUPERUSER_USERNAME', 'admin')
        email = os.getenv('SUPERUSER_EMAIL', 'admin@example.com')
        password = os.getenv('SUPERUSER_PASSWORD', 'admin123')

        user, created = user_model.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
            },
        )

        if created:
            user.set_password(password)
            user.save(update_fields=['password'])
            self.stdout.write(self.style.SUCCESS(f'Superuser created: {username}'))
            if password == 'admin123':
                self.stdout.write(self.style.WARNING('Change the default superuser password.'))
            return

        changed = False
        if not user.is_staff:
            user.is_staff = True
            changed = True
        if not user.is_superuser:
            user.is_superuser = True
            changed = True
        if not user.is_active:
            user.is_active = True
            changed = True
        if email and user.email != email:
            user.email = email
            changed = True

        if changed:
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Superuser updated: {username}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Superuser already exists: {username}'))

    def handle(self, *args, **kwargs):
        for group_name in ('ADMIN', 'GERENTE', 'FINANCEIRO'):
            group, created = Group.objects.get_or_create(name=group_name)
            action = 'Created' if created else 'Already exists'
            self.stdout.write(self.style.SUCCESS(f'{action}: "{group_name}"'))

        self._ensure_superuser()
