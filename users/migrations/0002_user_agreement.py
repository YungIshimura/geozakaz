# Generated by Django 3.2.18 on 2023-03-22 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='agreement',
            field=models.BooleanField(default=False, verbose_name='Принял условия соглашения'),
        ),
    ]
