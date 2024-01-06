# Generated by Django 4.2.5 on 2023-12-21 06:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0009_coupon_used_by'),
        ('core', '0024_remove_order_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productorder',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_orders', to='adminapp.product'),
        ),
    ]