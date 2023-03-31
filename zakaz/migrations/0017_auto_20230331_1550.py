# Generated by Django 3.2.18 on 2023-03-31 15:50

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zakaz', '0016_rename_cadastral_number_order_cadastral_numbers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cadastral_numbers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50, verbose_name='Кадастровый номер'), blank=True, null=True, size=None, verbose_name='Кадастровые номера'),
        ),
        migrations.AlterField(
            model_name='order',
            name='map',
            field=models.TextField(blank=True, null=True, verbose_name='Карта участка'),
        ),
    ]
