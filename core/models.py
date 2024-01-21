from django.db import models
from django.contrib.auth.models import User
from adminapp.models import Product
from django.db.models import Sum
from user.models import AddressUS, Coupon
from django.db.models import F


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    def update_total(self):
        total = self.cartitem_set.aggregate(total_price=Sum(models.F('quantity') * models.F('product__offer_price')))['total_price']
        self.total = total if total is not None else 0
        self.save()
        return self.total 

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.offer_price

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name} in order {self.cart}"

    def total_prices(self):
        return Sum(item.total_price() for item in self.cart.cartitem_set.all())


class Order(models.Model):
    STATUS = [
        ('New', 'New'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Returned', 'Returned'),
        ('pending', 'pending'),
        
    ]

    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order_number = models.CharField(max_length=200)
    address = models.ForeignKey(AddressUS, on_delete=models.SET_NULL, blank=True, null=True)
    order_total = models.FloatField()
    status = models.CharField(max_length=100, choices=STATUS, default='New')
    # payment_method = models.CharField(max_length=50, default='CashOnDelivery')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    # Add a ForeignKey relationship with Cart
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=True)

    order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    quantity = models.IntegerField(default=0)
    # Other fields...

    def save(self, *args, **kwargs):
        # Calculate and set the order_value before saving
        self.order_value = self.calculate_order_value()
        super().save(*args, **kwargs)

    def calculate_order_value(self):

        print("Calculating order value for Order ID:", self.id)
        discount_amount = self.coupon.discount_amount if self.coupon else 0
        print("Discount Amount:", discount_amount)
        calculated_value = self.order_total - discount_amount
        print("Calculated Order Value:", calculated_value)
        return calculated_value
        

        
class ProductOrder(models.Model):
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    address = models.ForeignKey(AddressUS, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Add the cart_item relationship
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE, null=True, blank=True)
    
    

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name} in order {self.order}, user {self.order.user}"
    

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100,default='Cancelled')
    amount_paid = models.FloatField(default=0)
    status = models.CharField(max_length=100)
    discount = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_method 
    
    