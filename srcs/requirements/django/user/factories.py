# pylint: disable=too-few-public-methods

import factory
from faker import Faker
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


User = get_user_model()
faker = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.LazyAttribute(lambda _: faker.unique.email())
    username = factory.LazyAttribute(lambda _: faker.unique.user_name())
    password = factory.LazyAttribute(lambda _: make_password(faker.password()))


class SignUpFactory(factory.Factory):
    class Meta:
        model = dict

    email = factory.LazyAttribute(lambda _: faker.unique.email())
    username = factory.LazyAttribute(lambda _: faker.unique.user_name())
    password = factory.Faker("password")
