from django.db import models

# 기본 유저 모델
class User (models.Model):
    id = models.AutoField(primary_key=True) # 기본키
    username = models.CharField(max_length=50, unique=True)
    nickname = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)  # 해싱된 비밀번호
