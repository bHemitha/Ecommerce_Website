from asyncio import AbstractServer
from itertools import count
from typing import AbstractSet
from django.db import models
from django.contrib.auth.models import User
from django.core import validators
from django.dispatch import receiver
from ckeditor.fields import RichTextField

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    email = models.EmailField(unique=True, default=None)
    phone_number = models.CharField(max_length=15, unique=True, default=None)
    def __str__(self):
        return self.user.username

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='product_images')
    discount = models.PositiveIntegerField(validators=[validators.MaxValueValidator(100)])
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.CharField(max_length=255, null=True, blank=True)
    rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    Product_details = RichTextField()
    is_top_deal = models.BooleanField(default=False)
    is_top_selling = models.BooleanField(default=False) 
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category_images/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    items = models.ManyToManyField(Product, through='CartItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    is_checked_out = models.BooleanField(default=False)
    def update_total_price(self):
        self.total_price = sum(item.cart_item_price for item in self.items.all())
        self.save()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    def save(self, *args, **kwargs):
        self.item_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=255)
    order_date = models.DateTimeField()
    shipment_date = models.DateTimeField()
    def __str__(self):
        return "order object"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return "orderitem object"