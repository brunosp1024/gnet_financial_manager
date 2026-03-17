from django.apps import apps
from django.contrib.auth.management import create_permissions
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


FIXTURES = [
    'initial_groups',
    'initial_users',
    'initial_customers',
    'initial_employees',
    'initial_invoices',
    'initial_transactions',
    'initial_notifications',
]

class Command(BaseCommand):
    help = 'Load initial fixtures'

    def _ensure_permissions(self):
        for app_config in apps.get_app_configs():
            create_permissions(app_config, verbosity=0)

        self.stdout.write(self.style.SUCCESS('Permissions created/updated'))

    def _load_initial_fixtures(self):
        for fixture_name in FIXTURES:
            try:
                call_command('loaddata', fixture_name)
                self.stdout.write(self.style.SUCCESS(f'Fixture loaded: {fixture_name}'))
            except Exception as exc:
                raise CommandError(f'Failed to load fixture "{fixture_name}": {exc}') from exc

    def handle(self, *args, **kwargs):
        self._ensure_permissions()
        self._load_initial_fixtures()
