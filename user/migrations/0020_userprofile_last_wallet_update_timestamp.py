# Generated by Django 4.2.5 on 2023-12-30 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_wallet_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='last_wallet_update_timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
