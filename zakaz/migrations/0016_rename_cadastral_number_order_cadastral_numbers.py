# Generated by Django 3.2.18 on 2023-03-31 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zakaz', '0015_auto_20230330_2140'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='cadastral_number',
            new_name='cadastral_numbers',
        ),
    ]
