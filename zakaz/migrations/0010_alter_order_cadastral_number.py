# Generated by Django 3.2.18 on 2023-03-28 11:36

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zakaz', '0009_rename_cadastral_region_number_area_cadastral_area_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cadastral_number',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50, verbose_name='Кадастровый номер'), size=None),
        ),
    ]
