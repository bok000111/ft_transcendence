from django.contrib.auth.models import AbstractUser
from django.db import models


# 기본 사용자 TODO: 추후에 확장할 수 있음
class User(AbstractUser):
    email = models.EmailField(
        max_length=128,
        unique=True,
    )
    oauth = models.BooleanField(default=False)

    first_name = None
    last_name = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["email", "username", "oauth"], name="unique_user"
            ),
        ]
