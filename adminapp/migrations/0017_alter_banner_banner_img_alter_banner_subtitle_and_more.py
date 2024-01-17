# Generated by Django 4.2.5 on 2024-01-17 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0016_banner_active_banner_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='banner_img',
            field=models.ImageField(blank=True, null=True, upload_to='media/banner/image'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='subtitle',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='banner',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]