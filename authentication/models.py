from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth.hashers import make_password


class CustomUserManager(BaseUserManager):

    def _create_user(self, username, email, password, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError("The given Username is not Valid")

        email = self.normalize_email(email)

        user = self.model(username=username, email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password, **extra_fields):
        user = self._create_user(username, email, password, is_active=True, is_staff=True, is_superuser=True,
                                 **extra_fields)
        user.save(using=self._db)


class User(AbstractBaseUser, PermissionsMixin):  # los fields que necesitamos agregar
    username = models.CharField(max_length=30, unique=True, blank=False, null=False)
    email = models.EmailField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(blank=True, null=True)
    user_image = models.CharField(max_length=400, unique=True, blank=True, null=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
