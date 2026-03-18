from django.apps import AppConfig


class CustomersConfig(AppConfig):
    name = 'apps.customers'

    def ready(self):
        from . import signals  # noqa: F401
