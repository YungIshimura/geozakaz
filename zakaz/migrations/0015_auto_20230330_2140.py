# Generated by Django 3.2.18 on 2023-03-30 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zakaz', '0014_auto_20230329_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coordinates',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Координаты'),
        ),
        migrations.AddField(
            model_name='order',
            name='map',
            field=models.FileField(default=[], upload_to='', verbose_name='Карта'),
            preserve_default=False,
        ),
    ]