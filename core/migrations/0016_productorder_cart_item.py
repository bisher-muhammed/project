# Generated by Django 4.2.5 on 2023-12-16 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_remove_productorder_cart_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='productorder',
            name='cart_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.cartitem'),
        ),
    ]