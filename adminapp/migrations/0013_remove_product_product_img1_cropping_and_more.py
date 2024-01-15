# Generated by Django 4.2.5 on 2024-01-09 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0012_product_product_img1_cropping_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_img1_cropping',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_img2_cropping',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_img3_cropping',
        ),
        migrations.AlterField(
            model_name='product',
            name='product_img1',
            field=models.ImageField(upload_to='media/product/img1'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_img2',
            field=models.ImageField(upload_to='media/product/img2'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_img3',
            field=models.ImageField(upload_to='media/product/img3'),
        ),
    ]
