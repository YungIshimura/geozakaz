# Generated by Django 3.2.18 on 2023-04-11 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zakaz', '0019_alter_order_map'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='height',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True, verbose_name='Высота'),
        ),
        migrations.AlterField(
            model_name='order',
            name='height_unit',
            field=models.CharField(blank=True, choices=[('m', 'м'), ('floor', 'этаж')], max_length=10, null=True, verbose_name='Еденица высота'),
        ),
        migrations.AlterField(
            model_name='order',
            name='width',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True, verbose_name='Ширина'),
        ),
        migrations.AlterField(
            model_name='order',
            name='width_unit',
            field=models.CharField(blank=True, choices=[('m', 'м'), ('кь', 'км')], max_length=10, null=True, verbose_name='Еденица ширины'),
        ),
    ]
