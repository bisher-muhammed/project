# Generated by Django 4.2.5 on 2023-12-09 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_order_discount_remove_order_shipping_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(default='CashOnDelivery', max_length=50),
        ),
    ]