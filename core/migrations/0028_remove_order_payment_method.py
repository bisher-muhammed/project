# Generated by Django 4.2.5 on 2023-12-22 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='payment_method',
        ),
    ]
