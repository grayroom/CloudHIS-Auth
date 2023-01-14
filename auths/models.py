from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User as _User

from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, username, name, dob, sex, password, email, address,
                    phone_number, user_type):
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username,
            name=name,
            dob=dob,
            sex=sex,
            email=email,
            address=address,
            phone_number=phone_number,
            user_type=user_type
        )
        # NOTE: 왜 얘만 따로 뻈지?
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_doctor(self, username, name, dob, sex, password, email, address,
                      phone_number, subject, position, user_type):
        user = self.create_user(
            username=username,
            name=name,
            dob=dob,
            sex=sex,
            password=password,
            email=email,
            address=address,
            phone_number=phone_number,
            user_type=user_type
        )
        user.subject = subject
        user.position = position
        # user.room = room
        # user.dept_idx = dept_idx
        # user.sup_idx = sup_idx
        user.save(using=self._db)

        return user

    def create_patient(self, username, name, dob, sex, password, email, address,
                       phone_number, user_type):
        user = self.create_user(
            username=username,
            name=name,
            dob=dob,
            sex=sex,
            password=password,
            email=email,
            address=address,
            phone_number=phone_number,
            user_type=user_type
        )
        user.save(using=self._db)
        return user


class User(_User):
    # 기본정보
    name = models.CharField(max_length=50)
    dob = models.DateField(null=False, blank=False)
    sex = models.CharField(max_length=10, null=False, blank=False)
    address = models.CharField(max_length=100)
    join_date = models.DateTimeField(auto_now_add=True)
    phone_number = PhoneNumberField()
    # 소속을 나타내는 칼럼들
    user_type = models.CharField(
        max_length=50, default='patient')  # patient, doctor, admin
    authority = models.IntegerField(default=0)  # 0: 외부, 1: 승인됨

    objects = UserManager()

    REQUIRED_FIELDS = ['alias']

    def __str__(self):
        return self.username

    def create_user(self, username, password, name, dob, sex, email, address,
                    phone_number, user_type, authority=0):
        user = User(
            username=username,
            password=password,
            name=name,
            dob=dob,
            sex=sex,
            email=email,
            address=address,
            phone_number=phone_number,
            user_type=user_type
        )
        user.save()
        return user


class Doctor(User):
    user_idx = models.OneToOneField(User, on_delete=models.CASCADE,
                                    parent_link=True, primary_key=True)
    subject = models.CharField(max_length=50)
    position = models.CharField(max_length=50)

    # 가입시 필수가 아님, 나중에 추가해야 할 정보
    room = models.CharField(max_length=50, null=True, default=None)
    dept_idx = models.IntegerField(null=True, default=None)
    sup_idx = models.IntegerField(null=True, default=None)

    def __str__(self):
        return self.username

    def create_doctor(self, username, password, name, dob, sex, email,
                      address, phone_number, subject, position, room,
                      dept_idx, sup_idx, user_type, authority=0):
        user = Doctor(
            username=username,
            password=password,
            name=name,
            dob=dob,
            sex=sex,
            email=email,
            address=address,
            phone_number=phone_number,
            subject=subject,
            position=position,
            room=room,
            dept_idx=dept_idx,
            sup_idx=sup_idx,
            user_type=user_type,
            authority=authority
        )
        user.save()
        return user


class Patient(User):
    user_idx = models.OneToOneField(User, on_delete=models.CASCADE,
                                    parent_link=True, primary_key=True)
    doc_idx = models.IntegerField(null=True, default=None)
    is_admission = models.BooleanField(null=True, default=None)
    room = models.CharField(max_length=50, null=True, default=None)

    def __str__(self):
        return self.username

    def create_patient(self, username, password, name, dob, sex, email,
                       address, phone_number, doc_idx, is_admission, room,
                       user_type, authority=0):
        user = Patient(
            username=username,
            password=password,
            name=name,
            dob=dob,
            sex=sex,
            email=email,
            address=address,
            phone_number=phone_number,
            doc_idx=doc_idx,
            is_admission=is_admission,
            room=room,
            user_type=user_type,
            authority=authority
        )
        user.save()
        return user
