# Generated by Django 4.2.5 on 2023-12-21 06:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_order_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
    ]