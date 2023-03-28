from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class User(AbstractUser):
    patronymic = models.CharField(
        'Отчество',
        max_length=30)
    phone = PhoneNumberField(
        'Телефон')
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
        'Уникальный номер заказа',
        max_length=8,
        unique=True,
        db_index=True,
        blank=True,
        null=True
    )
