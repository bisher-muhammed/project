# Generated by Django 4.2.5 on 2023-12-14 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0002_coupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='minimum_purchase',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
