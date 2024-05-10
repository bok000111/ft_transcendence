from django.contrib.auth import get_user_model
import factory
import faker

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.LazyAttribute(lambda _: f"{faker.Faker().email()}")
    username = factory.LazyAttribute(lambda _: f"{faker.Faker().user_name()}")
    password = factory.PostGenerationMethodCall(
        "set_password", faker.Faker().password()
    )


class SignUpFactory(factory.Factory):
    class Meta:
        model = dict

    email = factory.LazyAttribute(lambda _: f"{faker.Faker().email()}")
    username = factory.LazyAttribute(lambda _: f"{faker.Faker().user_name()}")
    password = factory.Faker("password")
