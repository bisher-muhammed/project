# Generated by Django 4.2.5 on 2023-12-07 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_userprofile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addressus',
            name='state',
            field=models.CharField(max_length=255),
        ),
    ]