import factory
from datetime import date
from faker import Faker
from apps.invoices.models import Invoice
from apps.customers.tests.factories import CustomerFactory

fake = Faker('pt_BR')


class InvoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Invoice

    customer = factory.SubFactory(CustomerFactory)
    value = factory.LazyFunction(lambda: fake.pydecimal(left_digits=4, right_digits=2, positive=True))
    due_date = factory.LazyFunction(lambda: fake.date_object())
    status = Invoice.Status.PENDING
    paid_at = None
