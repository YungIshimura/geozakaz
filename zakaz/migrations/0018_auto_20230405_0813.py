# Generated by Django 3.2.18 on 2023-04-05 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zakaz', '0017_auto_20230331_1550'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user_purpose_building',
        ),
        migrations.AlterField(
            model_name='order',
            name='purpose_building',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Пользовательское назначение здания'),
        ),
        migrations.AlterField(
            model_name='order',
            name='square_unit',
            field=models.CharField(choices=[('hectometer', 'га'), ('sq_m', 'м²')], max_length=10, verbose_name='Еденица площади'),
        ),
    ]
