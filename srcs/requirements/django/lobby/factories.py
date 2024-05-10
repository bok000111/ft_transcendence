import factory
import faker


class LobbyPostFactory(factory.Factory):
    class Meta:
        model = dict

    name = factory.LazyAttribute(lambda _: f"{faker.Faker().word()}")
    max_players = factory.Faker("random_int", min=2, max=4)
    end_score = factory.Faker("random_int", min=1, max=10)
