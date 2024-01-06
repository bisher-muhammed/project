# Generated by Django 4.2.5 on 2023-12-16 12:10

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_order_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productorder',
            name='address',
        ),
        migrations.RemoveField(
            model_name='productorder',
            name='order',
        ),
        migrations.AddField(
            model_name='productorder',
            name='cart_item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.cartitem'),
            preserve_default=False,
        ),
    ]
