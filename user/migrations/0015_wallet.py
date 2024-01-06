# Generated by Django 4.2.5 on 2023-12-13 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_wishlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.userprofile')),
            ],
        ),
    ]