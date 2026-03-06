import factory
from faker import Faker
from employees.models import Employee

fake = Faker('pt_BR')


class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Employee

    name       = factory.LazyFunction(lambda: fake.name())
    address    = factory.LazyFunction(lambda: fake.address())
    phone      = ''
    cpf        = ''
    position   = factory.LazyFunction(lambda: fake.job()[:100])
    modality   = Employee.Modality.CLT
    is_active  = True
    start_date = factory.LazyFunction(lambda: fake.date_object())
