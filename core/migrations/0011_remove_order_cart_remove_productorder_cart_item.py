# Generated by Django 4.2.5 on 2023-12-16 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_productorder_cart_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='productorder',
            name='cart_item',
        ),
    ]