# Generated by Django 4.2.5 on 2023-12-21 05:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0009_coupon_used_by'),
        ('core', '0022_order_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='adminapp.product'),
        ),
    ]
