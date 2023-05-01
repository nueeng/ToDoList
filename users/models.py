from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    '''유저 매니저 모델(validation, save to DB)'''
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    '''유저 모델'''
    GENDER_CHOICES = (
        ("M","Male"),
        ("F","Female"),
    )
    email = models.EmailField(
        verbose_name="이메일",
        max_length=255,
        unique=True,
    )
    name = models.CharField('이름', max_length=50)
    password = models.CharField('비밀번호', max_length=256)
    gender = models.CharField('성별', max_length=1, choices=GENDER_CHOICES)
    age = models.IntegerField('나이', null=True, blank=True)
    introduction = models.TextField('소개', null=True, blank=True, default="")
    is_active = models.BooleanField('활성화여부', default=True)
    is_admin = models.BooleanField('관리자여부', default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    