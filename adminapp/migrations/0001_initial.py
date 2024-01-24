# Generated by Django 4.2.5 on 2024-01-24 09:15

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner_img', models.ImageField(blank=True, null=True, upload_to='media/banner/image')),
                ('subtitle', models.CharField(blank=True, max_length=50, null=True)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('days_difference', models.IntegerField(blank=True, null=True)),
                ('expiry_date', models.DateField()),
            ],
        ),
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
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('expiry_date', models.DateField()),
                ('category', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='adminapp.category')),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_code', models.CharField(max_length=50, unique=True)),
                ('discount_amount', models.PositiveIntegerField()),
                ('minimum_purchase', models.IntegerField(default=0, null=True)),
                ('expiry_date', models.DateField()),
                ('is_blocked', models.BooleanField(default=False)),
                ('used_by', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
