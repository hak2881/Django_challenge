from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, nickname, email, password):
        if not email or not nickname:
            raise ValueError('이메일 또는 닉네임을 입력하세요')

        user = self.model(
            nickname=nickname,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db) # 현재 사용중인 데이터베이스 저장할때 사용
        return user

    def create_superuser(self, nickname, email, password):
        user = self.create_user(nickname, email, password)
        user.is_superuser = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser, PermissionsMixin):
    nickname = models.CharField('닉네임', max_length=20, unique=True)
    email = models.EmailField('이메일',max_length=40, unique=True)
    profile_image = models.ImageField(upload_to='users/profile_image', default='users/blank_profile_image.png')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    class Meta:
        verbose_name = '유저'
        verbose_name_plural = f'{verbose_name} 목록'