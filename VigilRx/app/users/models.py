from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):

    def create_superuser(self, username, role, address, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        return self.create_user(username, role, address, password, **other_fields)

    def create_user(self, username, role, address, password, **other_fields):
        if not username:
            raise ValueError('You must provide a username.')
        if not role:
            raise ValueError('You must provide a role.')
        if not address:
            raise ValueError('You must provide an address.')

        user = self.model(username=username, role=role, address=address, **other_fields)
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLES = {
        (1, 'Patient'),
        (2, 'Prescriber'),
        (3, 'Pharmacy'),
    }

    username = models.CharField(max_length=150, unique=True)
    role = models.PositiveIntegerField(verbose_name=('Role'), choices=ROLES, null=True)
    address = models.CharField(verbose_name=('Personal Blockchain Address'), max_length=42, unique=True)
    email = models.EmailField(verbose_name=('Email'), unique=True, null=True, blank=True)
    contract = models.CharField(verbose_name=('Role Contract Address'), max_length=42, unique=True, null=True, blank=True)
    identifier = models.CharField(verbose_name=('National Provider Identifier'), max_length=10, unique=True, null=True, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['role', 'address']

    def __str__(self):
        return self.username
