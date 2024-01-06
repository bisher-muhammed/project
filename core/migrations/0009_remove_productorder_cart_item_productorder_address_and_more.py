# Generated by Django 4.2.5 on 2023-12-16 12:10

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_wallet'),
        ('core', '0008_remove_productorder_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productorder',
            name='cart_item',
        ),
        migrations.AddField(
            model_name='productorder',
            name='address',
            field=models.ForeignKey(default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, to='user.addressus'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productorder',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.order'),
            preserve_default=False,
        ),
    ]
