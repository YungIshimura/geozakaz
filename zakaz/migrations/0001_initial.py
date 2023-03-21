# Generated by Django 3.2.18 on 2023-03-21 14:08

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название района')),
            ],
            options={
                'verbose_name': 'Район',
                'verbose_name_plural': 'Районы',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название города')),
                ('area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='citys', to='zakaz.area', verbose_name='Район')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='Имя заказчика')),
                ('surname', models.CharField(blank=True, max_length=250, verbose_name='Фамилия заказчика')),
                ('father_name', models.CharField(blank=True, max_length=250, verbose_name='Отчество заказчика')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Электронная почта заказчика')),
                ('cadastral_number', models.CharField(max_length=50, verbose_name='Кадастровый номер')),
                ('street', models.CharField(max_length=250, verbose_name='Улица')),
                ('house_number', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Номер дома')),
                ('building', models.PositiveBigIntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Строение/Корпус')),
                ('square', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Площадь участка')),
                ('square_unit', models.CharField(blank=True, choices=[('sq_m', 'м²'), ('hectometer', 'Га')], max_length=10, null=True, verbose_name='')),
                ('length', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Длина')),
                ('length_unit', models.CharField(blank=True, choices=[('m', 'м'), ('кь', 'км')], max_length=10, null=True, verbose_name='')),
                ('width', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Ширина')),
                ('width_unit', models.CharField(blank=True, choices=[('m', 'м'), ('кь', 'км')], max_length=10, null=True, verbose_name='')),
                ('height', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Высота')),
                ('height_unit', models.CharField(blank=True, choices=[('m', 'м'), ('floor', 'этаж')], max_length=10, null=True, verbose_name='')),
                ('title', models.TextField(verbose_name='Навзание объекта')),
                ('status', models.CharField(blank=True, choices=[('processed', 'Обработанная'), ('not processed', 'Не обработанная')], default='not processed', max_length=100, verbose_name='Статус заказа')),
                ('area', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, blank=True, chained_field='region', chained_model_field='region', null=True, on_delete=django.db.models.deletion.CASCADE, to='zakaz.area')),
                ('city', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='area', chained_model_field='area', on_delete=django.db.models.deletion.CASCADE, to='zakaz.city')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=180, verbose_name='Название региона')),
            ],
            options={
                'verbose_name': 'Регион',
                'verbose_name_plural': 'Регионы',
            },
        ),
        migrations.CreateModel(
            name='TypeWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50, verbose_name='Тип работы')),
            ],
            options={
                'verbose_name': 'Тип работы',
                'verbose_name_plural': 'Типы работ',
            },
        ),
        migrations.CreateModel(
            name='OrderFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='', verbose_name='Файл')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='zakaz.order', verbose_name='Заказы')),
            ],
            options={
                'verbose_name': 'Файлы к заказу',
                'verbose_name_plural': 'Файлы к заказам',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='zakaz.region', verbose_name='Регион'),
        ),
        migrations.AddField(
            model_name='order',
            name='type_work',
            field=models.ManyToManyField(related_name='orders', to='zakaz.TypeWork', verbose_name='Тип работы'),
        ),
        migrations.AddField(
            model_name='area',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='areas', to='zakaz.region', verbose_name='Регион'),
        ),
    ]