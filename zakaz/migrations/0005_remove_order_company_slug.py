# Generated by Django 3.2.18 on 2023-03-27 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zakaz', '0004_auto_20230327_1042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='company_slug',
        ),
    ]
