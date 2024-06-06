from django.contrib.auth import get_user_model
import factory
from faker import Faker

User = get_user_model()
faker = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.LazyFunction(faker.unique.email)
    username = factory.LazyFunction(faker.unique.user_name)
    password = factory.PostGenerationMethodCall("set_password", faker.password())


class SignUpFactory(factory.Factory):
    class Meta:
        model = dict

    email = factory.LazyFunction(faker.unique.email)
    username = factory.LazyFunction(faker.unique.user_name)
    password = factory.Faker("password")
