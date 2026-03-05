import factory
from datetime import date, datetime, time
from django.utils import timezone
from faker import Faker
from finance.models import Transaction
from customers.tests.factories import CustomerFactory

fake = Faker('pt_BR')


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    type = Transaction.Type.INCOME
    category = Transaction.Category.MONTHLY_FEE
    payment_method = Transaction.PaymentMethod.PIX
    description = factory.LazyFunction(lambda: fake.sentence(nb_words=4))
    value = factory.LazyFunction(lambda: fake.pydecimal(
        left_digits=4, right_digits=2, positive=True))
    customer = factory.SubFactory(CustomerFactory)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        explicit_created_at = kwargs.pop("created_at", None)
        explicit_date = kwargs.pop("date", None)

        instance = super()._create(model_class, *args, **kwargs)

        target = explicit_created_at if explicit_created_at is not None else explicit_date
        if target is None:
            return instance

        if isinstance(target, date) and not isinstance(target, datetime):
            dt = datetime.combine(target, time.min)
            target = timezone.make_aware(dt)
        elif timezone.is_naive(target):
            target = timezone.make_aware(target)

        instance.created_at = target
        instance.save(update_fields=["created_at"])
        return instance
