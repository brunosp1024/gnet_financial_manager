import factory
from faker import Faker
from notifications.models import Notification

fake = Faker('pt_BR')


class NotificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notification

    type = Notification.Type.ANOTHER
    message = factory.LazyFunction(lambda: fake.sentence(nb_words=6))
    is_read = False
