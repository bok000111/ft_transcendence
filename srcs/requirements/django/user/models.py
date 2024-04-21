from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser, BaseUserManager


# 사용자 매니저
class UserManager(BaseUserManager):
    def create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")
        if not password:
            raise ValueError("The Password field must be set")

        email = self.normalize_email(email)

        if self.model.objects.filter(email=email).exists():
            raise ValueError("Email is already in use.")
        if self.model.objects.filter(username=username).exists():
            raise ValueError("Username is already in use.")

        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, username, password, **extra_fields)


# 기본 사용자 TODO: 추후에 확장할 수 있음
class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    first_name = None
    last_name = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_email(self):
        return self.email

    def get_username(self):
        return self.username

    def set_password(self, raw_password: str | None) -> None:
        return super().set_password(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return super().check_password(raw_password)