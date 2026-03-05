import factory
from faker import Faker
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from users.models import User

fake = Faker('pt_BR')


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyFunction(lambda: fake.unique.user_name())
    first_name = factory.LazyFunction(lambda: fake.first_name())
    last_name = factory.LazyFunction(lambda: fake.last_name())
    email = factory.LazyFunction(lambda: fake.unique.email())
    is_active = True

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        for name in extracted:
            group, _ = Group.objects.get_or_create(name=name)
            self.groups.add(group)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        password = kwargs.pop("password", "senha@123")
        hash_password = kwargs.pop("hash_password", False)

        if hash_password:
            kwargs["password"] = make_password(password)
        else:
            kwargs["password"] = password

        return super()._create(model_class, *args, **kwargs)
