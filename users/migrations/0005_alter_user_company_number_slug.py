# Generated by Django 3.2.18 on 2023-03-30 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20230327_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='company_number_slug',
            field=models.SlugField(blank=True, max_length=8, null=True, unique=True, verbose_name='Уникальный номер компании'),
        ),
    ]