# Generated by Django 4.2.5 on 2023-12-14 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0004_alter_coupon_minimum_purchase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='minimum_purchase',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
