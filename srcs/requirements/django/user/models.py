from django.db import models
from django.contrib.auth.models import AbstractUser
from channels.db import database_sync_to_async


# 기본 사용자 TODO: 추후에 확장할 수 있음
class User(AbstractUser):
    email = models.EmailField(
        max_length=128,
        unique=True,
    )

    first_name = None
    last_name = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def set_password(self, raw_password: str | None) -> None:
        return super().set_password(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return super().check_password(raw_password)
