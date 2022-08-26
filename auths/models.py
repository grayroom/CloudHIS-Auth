from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager

class UserManager(UserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email,
                                password=password,
                                username=username)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
class User(AbstractBaseUser):
    id = models.BigAutoField(help_text="User ID", primary_key=True)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

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
        return self.username

    def get_short_name(self):
        return self.username

    def create_user(self, email, username, password):
        user = User(
            email=email,
            username=username,
            password=password
        )
        user.save()
        return user

    def __str__(self):
        return self.username

##############################################################################################
# NOTE: model manager -> http://blog.hwahae.co.kr/all/tech/tech-tech/4108/
# NOTE: custom user model -> https://dev-yakuza.posstree.com/ko/django/custom-user-model/
# NOTE: djgno.contrib.auth -> https://docs.djangoproject.com/en/4.1/ref/contrib/auth/
##############################################################################################