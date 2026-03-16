import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from customers.models import Customer
from employees.models import Employee
from finance.models import Transaction
from invoices.models import Invoice
from notifications.models import Notification
from users.models import User


GROUPS = {
    'ADMIN': {
        User: ['view', 'add', 'change', 'delete'],
        Customer: ['view', 'add', 'change', 'delete'],
        Employee: ['view', 'add', 'change', 'delete'],
        Transaction: ['view', 'add', 'change', 'delete'],
        Invoice: ['view', 'add', 'change', 'delete'],
        Notification: ['view'],
    },
    'GERENTE': {
        User: ['view', 'add', 'change', 'delete'],
        Customer: ['view', 'add', 'change', 'delete'],
        Employee: ['view', 'add', 'change', 'delete'],
        Transaction: ['view', 'add', 'change', 'delete'],
        Invoice: ['view', 'add', 'change', 'delete'],
        Notification: ['view'],
    },
    'FINANCEIRO': {
        User: ['view'],
        Customer: ['view', 'add', 'change'],
        Employee: ['view'],
        Transaction: ['view', 'add', 'change', 'delete'],
        Invoice: ['view', 'add', 'change', 'delete'],
        Notification: ['view'],
    },
}


class Command(BaseCommand):
    help = 'Create/update groups with permissions and ensure initial superuser'

    def _get_model_permissions(self, model_class, actions):
        content_type = ContentType.objects.get_for_model(model_class)
        model_name = model_class._meta.model_name
        expected_codenames = [f'{action}_{model_name}' for action in actions]
        permissions = list(
            Permission.objects.filter(
                content_type=content_type,
                codename__in=expected_codenames,
            )
        )

        found_codenames = {permission.codename for permission in permissions}
        missing_codenames = [
            codename for codename in expected_codenames if codename not in found_codenames
        ]

        if missing_codenames:
            self.stdout.write(
                self.style.WARNING(
                    f'Missing permissions for {model_class.__name__}: {", ".join(missing_codenames)}'
                )
            )

        return permissions

    def _sync_groups_permissions(self):
        for group_name, model_permissions in GROUPS.items():
            group, created = Group.objects.get_or_create(name=group_name)
            action = 'Created' if created else 'Already exists'
            self.stdout.write(self.style.SUCCESS(f'{action}: "{group_name}"'))

            desired_permission_ids = set()
            for model_class, actions in model_permissions.items():
                permissions = self._get_model_permissions(model_class, actions)
                desired_permission_ids.update(permission.id for permission in permissions)

            current_permission_ids = set(group.permissions.values_list('id', flat=True))
            if current_permission_ids != desired_permission_ids:
                group.permissions.set(desired_permission_ids)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Permissions synced: "{group_name}" ({len(desired_permission_ids)} permissions)'
                    )
                )
            else:
                self.stdout.write(self.style.SUCCESS(f'Permissions already synced: "{group_name}"'))

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
        self._sync_groups_permissions()
        self._ensure_superuser()
