from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User as _User

from phonenumber_field.modelfields import PhoneNumberField

from django.core.validators import RegexValidator
from django.contrib import auth


class UserManager(BaseUserManager):
    def create_user(self, alias, name, password=None):
        if not alias:
            raise ValueError('Users must have an alias')

        user = self.model(
            alias=alias,
            name=name
        )
        # NOTE: 왜 얘만 따로 뻈지?
        user.set_password(password)

        user.save(using=self._db)
        return user


class User(_User):
    name = models.CharField(max_length=50)
    alias = models.CharField(max_length=50)  # 얘가 진짜 로그인할때 쓰는 아이디
    authority = models.IntegerField(default=0)  # 0: 일반사용자, 1: 관리자

    objects = UserManager()

    USERNAME_FIELD = 'alias'
    REQUIRED_FIELDS = ['alias']

    def __str__(self):
        return self.alias

    def create_user(self, alias, password, name):
        user = User(
            alias=alias,
            password=password,
            name=name
        )
        user.save()
        return user


class UserInfoManager(models.Manager):
    def create_user_info(self, user_id, name, email, address, subject, phone_number):
        user_info = self.model(
            user_id=user_id,
            name=name,
            email=email,
            address=address,
            subject=subject,
            phone_number=phone_number
        )
        user_info.save(using=self._db)
        return user_info


class UserInformation(models.Model):
    id = models.BigAutoField(
        help_text="User ID", primary_key=True)  # 로그인 아이디가 아니라 PK
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column="user_id")

    # 기본정보
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    join_date = models.DateTimeField(auto_now_add=True)
    phone_number = PhoneNumberField()

    # 소속을 나타내는 칼럼들
    subject = models.CharField(max_length=50)

    objects = UserInfoManager()

    def create_user_information(user_id, name, email, address, subject, phone_number):
        user_information = UserInformation(
            user_id=user_id,
            name=name,
            address=address,
            email=email,
            subject=subject,
            phone_number=phone_number
        )
        user_information.save()
        return user_information


##############################################################################################
# NOTE: model manager -> http://blog.hwahae.co.kr/all/tech/tech-tech/4108/
# NOTE: custom user model -> https://dev-yakuza.posstree.com/ko/django/custom-user-model/
# NOTE: djgno.contrib.auth -> https://docs.djangoproject.com/en/4.1/ref/contrib/auth/
##############################################################################################
