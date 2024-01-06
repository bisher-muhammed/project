from django.db import models
from django.core.validators import MinValueValidator


class  Category(models.Model):
    category_name=models.CharField(100,null=True,blank=True)
    description=models.TextField()
    category_image=models.ImageField(upload_to='media/category', null=False, blank=False)
    is_blocked=models.BooleanField(default=False)


    def __str__(self):
        return self.category_name
    

class Brand(models.Model):
    brand_name=models.CharField(max_length=100,unique=True)
    brand_description =models.TextField(max_length=400)
    brand_image=models.ImageField(upload_to='media/brands', blank=True, null=True)
    is_active = models.BooleanField(default=True) 
    def __str__(self):
        return self.brand_name



class Size(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True) 


    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    

    product_name = models.CharField(max_length=100)
    product_description = models.TextField(max_length=400)
    original_price = models.IntegerField(validators=[MinValueValidator(0)])
    offer_price = models.IntegerField(validators=[MinValueValidator(0)])
    
    product_img1 = models.ImageField(upload_to='media/product/img1', blank=False, null=False)
    product_img2 = models.ImageField(upload_to='media/product/img2', blank=False, null=False)
    product_img3 = models.ImageField(upload_to='media/product/img3', blank=False, null=False)
    
    sizes = models.ManyToManyField(Size, related_name='products', blank=True)
    colors = models.ManyToManyField(Color, related_name='products', blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.product_name
    

class Coupon(models.Model):
    coupon_code = models.CharField(max_length=50,unique=True)
    discount_amount = models.PositiveIntegerField()
    minimum_purchase = models.IntegerField(null=True, default=0)

    expiry_date= models.DateField()
    is_blocked=models.BooleanField(default=False)
    

    def __str__(self):
        return self.coupon_code
    
    