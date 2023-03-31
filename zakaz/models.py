from django.db import models
from django.core.validators import MinValueValidator
from smart_selects.db_fields import ChainedForeignKey
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField

User = get_user_model()


class TypeWork(models.Model):
    type = models.CharField(
        'Тип работы',
        max_length=50
    )

    def __str__(self):
        return f'{self.type}'

    class Meta:
        verbose_name = 'Тип работы'
        verbose_name_plural = 'Типы работ'


class Region(models.Model):
    name = models.CharField(
        'Название региона',
        max_length=180
    )
    cadastral_region_number = models.CharField(
        'Кадастровый номер',
        max_length=2,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'


class Area(models.Model):
    name = models.CharField(
        'Название района',
        max_length=200
    )
    cadastral_area_number = models.CharField(
        'Кадастровый номер',
        max_length=2,
        blank=True,
        null=True
    )
    region = models.ForeignKey(
        Region,
        related_name='areas',
        on_delete=models.CASCADE,
        verbose_name='Регион',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'


class City(models.Model):
    name = models.CharField(
        'Название города',
        max_length=100
    )
    area = models.ForeignKey(
        Area,
        related_name='citys',
        on_delete=models.CASCADE,
        verbose_name='Район',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class PurposeBuilding(models.Model):
    purpose = models.CharField(
        'Назначение',
        max_length=150
    )

    def __str__(self):
        return f'{self.purpose}'

    class Meta:
        verbose_name = 'Назначение здания'
        verbose_name_plural = 'Назначения зданий'


class WorkObjective(models.Model):
    objective = models.CharField(
        'Цель работы',
        max_length=150
    )

    def __str__(self):
        return f'{self.objective}'

    class Meta:
        verbose_name = 'Цель работы'
        verbose_name_plural = 'Цели работ'


class Order(models.Model):
    SQUARE_UNIT = (
        ('sq_m', 'м²'),
        ('hectometer', 'га')
    )
    LENGTH_AND_WIDTH_UNIT = (
        ('m', 'м'),
        ('кь', 'км')
    )
    HEIGHT_UNIT = (
        ('m', 'м'),
        ('floor', 'этаж')
    )
    name = models.CharField(
        'Имя заказчика',
        max_length=100,
    )
    surname = models.CharField(
        'Фамилия заказчика',
        max_length=250,
    )
    father_name = models.CharField(
        'Отчество заказчика',
        max_length=250,
        blank=True,
        null=True
    )
    phone_number = PhoneNumberField(
        'Номер телефона'
    )
    email = models.EmailField(
        "Электронная почта заказчика",
        max_length=254,
        blank=True
    )
    cadastral_numbers = ArrayField(models.CharField(
        'Кадастровый номер',
        max_length=50,
    ), blank=True, null=True, verbose_name='Кадастровые номера')
    region = models.ForeignKey(
        Region,
        related_name='orders',
        on_delete=models.CASCADE,
        verbose_name='Регион'
    )
    area = ChainedForeignKey(
        Area,
        chained_field='region',
        chained_model_field='region',
        show_all=False,
        auto_choose=True,
        sort=True
    )
    city = ChainedForeignKey(
        City,
        chained_field='area',
        chained_model_field='area',
        show_all=False,
        auto_choose=True,
        sort=True
    )
    street = models.CharField(
        'Улица',
        max_length=250,
    )
    house_number = models.PositiveIntegerField(
        'Номер дома',
        validators=[MinValueValidator(0)]
    )
    building = models.PositiveBigIntegerField(
        'Строение/Корпус',
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
    )
    square = models.DecimalField(
        'Площадь участка',
        max_digits=8,
        decimal_places=3
    )
    square_unit = models.CharField(
        'Еденица площади',
        max_length=10,
        choices=SQUARE_UNIT,
    )
    length = models.DecimalField(
        'Длина',
        max_digits=8,
        decimal_places=3
    )
    length_unit = models.CharField(
        'Еденица длины',
        max_length=10,
        choices=LENGTH_AND_WIDTH_UNIT,
    )
    width = models.DecimalField(
        'Ширина',
        max_digits=8,
        decimal_places=3
    )
    width_unit = models.CharField(
        'Еденица ширины',
        max_length=10,
        choices=LENGTH_AND_WIDTH_UNIT,
    )
    height = models.DecimalField(
        'Высота',
        max_digits=8,
        decimal_places=3
    )
    height_unit = models.CharField(
        'Еденица высота',
        max_length=10,
        choices=HEIGHT_UNIT,
    )
    type_work = models.ManyToManyField(
        TypeWork,
        related_name='orders',
        verbose_name='Виды работ',
    )
    comment = models.TextField(
        'Комментарий',
        blank=True
    )
    date = models.DateTimeField(
        'Дата заявки',
        auto_now_add=True,
    )
    purpose_building = models.ForeignKey(
        PurposeBuilding,
        on_delete=models.CASCADE,
        verbose_name='Назначение здания',
        related_name='orders',
        blank=True,
        null=True
    )
    user_purpose_building = models.CharField(
        'Пользовательское назначение здания',
        max_length=200,
        blank=True,
        null=True
    )
    work_objective = models.ForeignKey(
        WorkObjective,
        on_delete=models.CASCADE,
        verbose_name='Цель работы',
        related_name='orders',
    )
    object_name = models.CharField(
        'Название объекта',
        max_length=200,
        blank=True,
        null=True
    )

    coordinates = models.CharField(
        'Координаты',
        max_length=1000,
        blank=True,
        null=True)

    map = models.TextField(
        'Карта участка',
        null=True,
        blank=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', null=True, blank=True)

    def __str__(self):
        return f'Заказ для {self.user.company_name}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderFile(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='Заказы'
    )
    file = models.FileField(
        'Файл'
    )

    def __str__(self):
        return f'Файлы к заказу номер {self.order}'

    class Meta:
        verbose_name = 'Файлы к заказу'
        verbose_name_plural = 'Файлы к заказам'


# Модели необходимые для выгрузки DOCX
class Department(models.Model):
    region = models.ForeignKey(
        Region,
        related_name='region_department',
        on_delete=models.CASCADE,
        verbose_name='Регион ведомства',
    )
    name = models.CharField(
        'Название ведомства',
        max_length=250
    )
    director_position = models.CharField(
        'Должность руководителя ведомства',
        max_length=150
    )
    director_name = models.CharField(
        'Имя руководителя',
        max_length=20
    )
    director_surname = models.CharField(
        'Фамилия руководителя',
        max_length=50
    )
    director_patronymic = models.CharField(
        'Отчество руководителя',
        max_length=30
    )
    phone_number = PhoneNumberField(
        'Телефон ведомства'
    )
    email = models.EmailField(
        "Электронная почта ведомства",
        max_length=254
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Ведомство'
        verbose_name_plural = 'Ведомства'
