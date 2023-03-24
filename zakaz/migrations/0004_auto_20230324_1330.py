# Generated by Django 3.2.18 on 2023-03-24 10:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('zakaz', '0003_auto_20230323_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='order',
            name='comment',
            field=models.TextField(verbose_name='Название объекта'),
        ),
        migrations.AlterField(
            model_name='order',
            name='work_objective',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='zakaz.workobjective', verbose_name='Цель работы'),
        ),
    ]