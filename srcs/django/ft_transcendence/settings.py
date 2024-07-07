"""
Django settings for ft_transcendence project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path
from corsheaders.defaults import default_methods, default_headers

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

DEBUG = os.getenv("DJANGO_DEBUG") == "True"
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# TODO: 나중에 환경변수로 변경
ALLOWED_HOSTS = [
    os.getenv("HOST_NAME")
]
CSRF_TRUSTED_ORIGINS = [
    f"http://{os.getenv('HOST_NAME')}",
    f"https://{os.getenv('HOST_NAME')}",
]
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "Lax"

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    f"http://{os.getenv('HOST_NAME')}",
    f"https://{os.getenv('HOST_NAME')}",
]
CORS_ALLOW_METHODS = [
    *default_methods,
]
CORS_ALLOW_HEADERS = (
    *default_headers,
    "access-control-allow-origin",
    "origin",
)

# Application definition
INSTALLED_APPS = [
    "daphne",  # daphne - ASGI 서버
    "corsheaders",  # cors - cross-origin resource sharing
    "ft_transcendence",  # 프로젝트 설정
    "api",  # api 라우팅
    "ws",  # websocket 라우팅
    "oauth",  # 42 OAuth
    "user",  # 유저 관리
    "result",  # 결과 페이지 - 블록체인으로 관리
    "channels",  # channels - websocket
    "django.contrib.auth",  # JWT 사용으로 세션은 사용 안하지만 보안기능 사용
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "user.middleware.JWTAuthMiddleware",
]

ROOT_URLCONF = "ft_transcendence.urls"
CHANNEL_URLCONF = "ws.routing"
WSGI_APPLICATION = "ft_transcendence.wsgi.application"
ASGI_APPLICATION = "ft_transcendence.asgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
    }
}

# Password, User, Authentication
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
AUTH_USER_MODEL = "user.User"
AUTHENTICATION_BACKENDS = [
    "user.backends.JWTAuthenticationBackend",
]

# JWT
JWT_ALGORITHM = "HS256"  # HMAC SHA-256
JWT_SECRET_KEY = SECRET_KEY  # use django secret key
JWT_REFRESH_TOKEN_LIFETIME = 60 * 60 * 24 * 30  # 30 days
JWT_ACCESS_TOKEN_LIFETIME = 60 * 60  # 1 hour
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = "static/"
STATIC_ROOT = "/var/www/ft/"
STATICFILES_DIRS = [  # 개발시에만 사용
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Django Channels
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                (
                    os.getenv("REDIS_HOST"),
                    os.getenv("REDIS_PORT"),
                )
            ],
        },
    },
}


# 42 OAuth
OAUTH_42_URL = os.getenv("OAUTH_42_URL")
OAUTH_42_CLIENT_ID = os.getenv("OAUTH_42_CLIENT_ID")
OAUTH_42_CLIENT_SECRET = os.getenv("OAUTH_42_CLIENT_SECRET")
OAUTH_42_REDIRECT_URI = os.getenv("OAUTH_42_REDIRECT_URI")
OAUTH_42_TOKEN_URL = os.getenv("OAUTH_42_TOKEN_URL")

# Email 2FA
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("EMAIL_HOST_USER")
OTP_CODE_EXPIRE_SECONDS = 60 * 5  # 5 minutes

# Silence system check
# self-signed certificate를 사용하면서 hsts를 사용하면 브라우저에서 접속이 안될 수 있어서 비활성화
SILENCED_SYSTEM_CHECKS = ["security.W004"]
