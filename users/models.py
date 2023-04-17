from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from phonenumber_field.modelfields import PhoneNumberField
from pytils.translit import slugify


class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        if not phone_number:
            raise ValueError('Phone number must be set')
        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, phone_number, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(Q(email=username) | Q(phone_number=username))


class User(AbstractUser):
    username = None
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=255,
        unique=True)
    phone_number = PhoneNumberField(
        'Номер телефона',
        unique=True,
        null=True,
        blank=True)
    agreement = models.BooleanField(
        'Принял условия соглашения',
        default=False)
    company_name = models.CharField(
        'Название компании',
        max_length=150,
        null=True,
        blank=True
    )
    company_slug = models.SlugField(
        'Слаг компании',
        max_length=150,
        blank=True,
        null=True
    )
    company_number_slug = models.SlugField(
        'Уникальный номер компании',
        max_length=8,
        unique=True,
        db_index=True,
        blank=True,
        null=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def save(self, *args, **kwargs):
        self.company_slug = slugify(self.company_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
