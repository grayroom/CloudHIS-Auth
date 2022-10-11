from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User as _User

from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, username, name, password, email, address,
                    phone_number):
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username,
            name=name,
            email=email,
            address=address,
            phone_number=phone_number
        )
        # NOTE: 왜 얘만 따로 뻈지?
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_doctor(self, username, name, password, email, address,
                      phone_number, subject):
        user = self.create_user(
            username=username,
            name=name,
            password=password,
            email=email,
            address=address,
            phone_number=phone_number
        )
        user.subject = subject
        # user.room = room
        # user.dept_idx = dept_idx
        # user.sup_idx = sup_idx
        user.save(using=self._db)

        return user

    def create_patient(self, username, name, password, email, address,
                       phone_number, doc_idx, is_admission, room):
        user = self.create_user(
            username=username,
            name=name,
            password=password,
            email=email,
            address=address,
            phone_number=phone_number
        )
        user.doc_idx = doc_idx
        user.is_admission = is_admission
        user.room = room
        user.save(using=self._db)
        return user


class User(_User):
    # 기본정보
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    join_date = models.DateTimeField(auto_now_add=True)
    phone_number = PhoneNumberField()
    # 소속을 나타내는 칼럼들
    authority = models.IntegerField(default=0)  # 0: 외부, 1: 의사, 2: 관리자

    objects = UserManager()

    REQUIRED_FIELDS = ['alias']

    def __str__(self):
        return self.username

    def create_user(self, username, password, name, email, address,
                    phone_number):
        user = User(
            username=username,
            password=password,
            name=name,
            email=email,
            address=address,
            phone_number=phone_number
        )
        user.save()
        return user


class Doctor(User):
    user_idx = models.OneToOneField(User, on_delete=models.CASCADE,
                                    parent_link=True, primary_key=True)
    subject = models.CharField(max_length=50)
    room = models.CharField(max_length=50, null=True, default=None)
    dept_idx = models.IntegerField(null=True, default=None)
    sup_idx = models.IntegerField(null=True, default=None)

    def __str__(self):
        return self.username

    def create_doctor(self, username, password, name, email, address,
                      phone_number, subject, room, dept_idx, sup_idx):
        user = Doctor(
            username=username,
            password=password,
            name=name,
            email=email,
            address=address,
            phone_number=phone_number,
            subject=subject,
            room=room,
            dept_idx=dept_idx,
            sup_idx=sup_idx
        )
        user.save()
        return user


class Patient(User):
    user_idx = models.OneToOneField(User, on_delete=models.CASCADE,
                                    parent_link=True, primary_key=True)
    doc_idx = models.IntegerField(default=0)
    is_admission = models.BooleanField(default=False)
    room = models.CharField(max_length=50)

    def __str__(self):
        return self.username

    def create_patient(self, username, password, name, email, address,
                       phone_number, doc_idx, is_admission, room):
        user = Patient(
            username=username,
            password=password,
            name=name,
            email=email,
            address=address,
            phone_number=phone_number,
            doc_idx=doc_idx,
            is_admission=is_admission,
            room=room
        )
        user.save()
        return user
