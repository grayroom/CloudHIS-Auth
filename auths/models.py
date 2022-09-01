from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
# from phonenumber_field.modelfields import PhoneNumberField

class UserManager(BaseUserManager):
    def create_user(self, email, alias, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            alias=alias,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, alias, password):
        user = self.create_user(email,
                                password=password,
                                alias=alias,
                                )

        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    id = models.BigAutoField(help_text="User ID", primary_key=True) # 로그인 아이디가 아니라 PK
    
    alias = models.CharField(max_length=50) # 얘가 진짜 로그인할때 쓰는 아이디
    password = models.CharField(max_length=128)
    authority = models.IntegerField(default=0) # 0: 일반사용자, 1: 관리자
    last_login = models.DateTimeField(auto_now_add=True)
    email = models.CharField(max_length=50)

    objects = UserManager()

    alias_FIELD = 'alias'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.alias

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_superuser(self):
        return True

    def get_full_name(self):
        return self.alias

    def get_short_name(self):
        return self.alias

    def create_user(self, email, alias, password):
        user = User(
            email=email,
            alias=alias,
            password=password,
        )
        user.save()
        return user

    def __str__(self):
        return self.alias

class UserInformation:
    id = models.BigAutoField(help_text="User ID", primary_key=True)  # 로그인 아이디가 아니라 PK

    # 기본정보
    name = models.CharField(max_length=50)
    # phone_number = PhoneNumberField(unique=True)
    address = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    join_date = models.DateTimeField(auto_now_add=True)
    
    # 소속을 나타내는 칼럼들
    subject = models.CharField(max_length=50)


##############################################################################################
# NOTE: model manager -> http://blog.hwahae.co.kr/all/tech/tech-tech/4108/
# NOTE: custom user model -> https://dev-yakuza.posstree.com/ko/django/custom-user-model/
# NOTE: djgno.contrib.auth -> https://docs.djangoproject.com/en/4.1/ref/contrib/auth/
##############################################################################################