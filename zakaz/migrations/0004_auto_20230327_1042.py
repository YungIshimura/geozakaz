# Generated by Django 3.2.18 on 2023-03-27 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zakaz', '0003_auto_20230325_0918'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='slug',
            new_name='number_slug',
        ),
        migrations.AddField(
            model_name='order',
            name='company_slug',
            field=models.SlugField(blank=True, max_length=250, null=True, unique=True, verbose_name='Слаг компании'),
        ),
    ]
