from smtplib import SMTPException
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
from django.conf import settings
from django.utils import timezone
import random


# 기본 사용자 TODO: 추후에 확장할 수 있음
class User(AbstractUser):
    email = models.EmailField(
        max_length=128,
        unique=True,
    )
    oauth = models.BooleanField(default=False)
    otp_code = models.CharField(max_length=6, null=True)
    otp_code_created_at = models.DateTimeField(null=True)

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

    def __str__(self):
        return self.email

    def generate_otp_code(self) -> str:
        code = str(random.randint(0, 999999))
        code.zfill(6)
        return code

    @transaction.atomic
    def send_otp_code(self):
        self.otp_code = self.generate_otp_code()
        self.otp_code_created_at = timezone.now()
        print(self.otp_code)
        try:
            print(f"Your OTP Code is {self.otp_code}")
            # send_mail(
            #     "OTP Code",
            #     f"Your OTP Code is {self.otp_code}",
            #     settings.DEFAULT_FROM_EMAIL,
            #     recipient_list=[self.email],
            #     fail_silently=False,
            # )
        except SMTPException:
            return False
        else:
            self.save()
            return True

    @classmethod
    @transaction.atomic
    def verify_otp_code(cls, code):
        try:
            user = cls.objects.get(otp_code=code)
        except cls.DoesNotExist:
            return None

        if user.otp_code_created_at < timezone.now() - timezone.timedelta(minutes=5):
            return None

        user.otp_code = None
        user.otp_code_created_at = None
        user.save()
        return user
