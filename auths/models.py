from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User as _User

from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, username, name, password, email, address, subject, phone_number):
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username,
            name=name,
            email=email,
            address=address,
            subject=subject,
            phone_number=phone_number

        )
        # NOTE: 왜 얘만 따로 뻈지?
        user.set_password(password)

        user.save(using=self._db)
        return user


class User(_User):
    # 기본정보
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    join_date = models.DateTimeField(auto_now_add=True)
    phone_number = PhoneNumberField()
    # 소속을 나타내는 칼럼들
    subject = models.CharField(max_length=50)
    authority = models.IntegerField(default=0)  # 0: 일반사용자, 1: 관리자

    objects = UserManager()

    REQUIRED_FIELDS = ['alias']

    def __str__(self):
        return self.username

    def create_user(self, username, password, name, email, address, subject, phone_number):
        user = User(
            username=username,
            password=password,
            name=name,
            email=email,
            address=address,
            subject=subject,
            phone_number=phone_number
        )
        user.save()
        return user

##############################################################################################
# NOTE: model manager -> http://blog.hwahae.co.kr/all/tech/tech-tech/4108/
# NOTE: custom user model -> https://dev-yakuza.posstree.com/ko/django/custom-user-model/
# NOTE: djgno.contrib.auth -> https://docs.djangoproject.com/en/4.1/ref/contrib/auth/
##############################################################################################
