import random
from smtplib import SMTPException
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser
from django.db import models, transaction
from django.conf import settings
from django.utils import timezone


class User(AbstractBaseUser):
    username = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)
    is_oauth_user = models.BooleanField(default=False)
    otp_code = models.CharField(max_length=6, null=True)
    otp_code_created_at = models.DateTimeField(null=True)

    last_login = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "is_oauth_user"]

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["email", "is_oauth_user"], name="unique_user_per_service"
            ),
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._access_token = None
        self._is_access_token_modified = False

    def set_access_token(self, access_token):
        self._access_token = access_token

    def change_access_token(self, access_token):
        self._access_token = access_token
        self._is_access_token_modified = True

    def get_access_token(self):
        return self._access_token

    @property
    def is_access_token_modified(self):
        return self._is_access_token_modified

    def generate_otp_code(self) -> str:
        return f"{random.randint(0, 999999):06d}"  # 6자리로 패딩된 OTP 코드 생성

    @transaction.atomic
    def send_otp_code(self):
        self.otp_code = self.generate_otp_code()
        self.otp_code_created_at = timezone.now()

        try:
            send_mail(
                "OTP Code",
                f"Your OTP Code is {self.otp_code}",
                settings.DEFAULT_FROM_EMAIL,
                [self.email],  # recipient_list는 리스트여야 함
                fail_silently=False,
            )
        except SMTPException:
            self.otp_code = None  # 롤백: 인증 코드 초기화
            self.otp_code_created_at = None
            return False

        self.save()
        return True

    @classmethod
    @transaction.atomic
    def verify_otp_code(cls, code):
        try:
            user = cls.objects.get(otp_code=code)
        except cls.DoesNotExist:
            return None

        # OTP 코드의 유효 시간 설정 (분 단위)
        if user.otp_code_created_at < timezone.now() - timezone.timedelta(
            seconds=settings.OTP_CODE_EXPIRE_SECONDS
        ):
            # 만료된 OTP 코드는 삭제하고 None을 반환
            user.otp_code = None
            user.otp_code_created_at = None
            user.save()
            return None

        # 유효한 경우 OTP 코드 삭제 후 유저 객체 반환
        user.otp_code = None
        user.otp_code_created_at = None
        user.save()
        return user
