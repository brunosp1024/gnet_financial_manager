import factory
from faker import Faker
from customers.models import Customer

fake = Faker('pt_BR')


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    name       = factory.LazyFunction(lambda: fake.name())
    address    = factory.LazyFunction(lambda: fake.address())
    phone      = ''
    cpf        = ''
    is_active  = True
    start_date = factory.LazyFunction(lambda: fake.date_object())
