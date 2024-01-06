# Generated by Django 4.2.5 on 2023-12-05 06:27

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=100, unique=True)),
                ('brand_description', models.TextField(max_length=400)),
                ('brand_image', models.ImageField(blank=True, null=True, upload_to='media/brands')),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(blank=True, null=True, verbose_name=100)),
                ('description', models.TextField()),
                ('category_image', models.ImageField(upload_to='media/category')),
                ('is_blocked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('product_description', models.TextField(max_length=400)),
                ('original_price', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('offer_price', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('product_img1', models.ImageField(upload_to='media/product/img1')),
                ('product_img2', models.ImageField(upload_to='media/product/img2')),
                ('product_img3', models.ImageField(upload_to='media/product/img3')),
                ('is_active', models.BooleanField(default=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.category')),
                ('colors', models.ManyToManyField(blank=True, related_name='products', to='adminapp.color')),
                ('sizes', models.ManyToManyField(blank=True, related_name='products', to='adminapp.size')),
            ],
        ),
    ]