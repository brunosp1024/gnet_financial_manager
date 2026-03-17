import pytest
from django.utils import timezone

from apps.customers.models import Customer
from apps.customers.signals import customer_created_notification
from apps.notifications.models import Notification


@pytest.mark.django_db
class TestCustomerSignals:

	def test_customer_created_creates_notification(self):
		customer = Customer(name="Cliente Teste")

		customer_created_notification(
			sender=Customer,
			instance=customer,
			created=True,
		)

		notification = Notification.objects.get()
		assert notification.type == Notification.Type.NEW_CUSTOMER
		assert notification.message == "Novo cliente cadastrado: Cliente Teste"

	def test_customer_updated_does_not_create_notification(self):
		customer = Customer(name="Cliente Atualizado")

		customer_created_notification(
			sender=Customer,
			instance=customer,
			created=False,
		)

		assert Notification.objects.count() == 0

	def test_customer_deleted_does_not_create_notification(self):
		customer = Customer(
			name="Cliente Removido",
			deleted_at=timezone.now(),
		)

		customer_created_notification(
			sender=Customer,
			instance=customer,
			created=True,
		)

		assert Notification.objects.count() == 0


