# Generated by Django 3.2.18 on 2023-03-28 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zakaz', '0008_area_cadastral_region_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='area',
            old_name='cadastral_region_number',
            new_name='cadastral_area_number',
        ),
    ]
