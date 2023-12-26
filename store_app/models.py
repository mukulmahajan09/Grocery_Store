from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class ProductCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return self.category_name
    
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=200, blank=False, null=False)
    product_desc = models.TextField(blank=False, null=False)
    product_image = models.ImageField(upload_to='product_images/', blank=False, null=False)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_status = models.PositiveIntegerField()

    def __str__(self):
        return self.product_name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = PhoneNumberField(unique=True, blank=True, null=True)
    shipping_address = models.TextField(blank=True, null=True)
    billing_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.customer_name
    
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product)
    order_datetime = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=100, choices=[('pending', 'Pending'), ('paid', 'Paid'), ('failed', 'Failed')])
    payment_status = models.CharField(max_length=100, choices=[('pending', 'Pending'), ('paid', 'Paid'), ('failed', 'Failed')])
    payment_status = models.BooleanField(default=False)
    order_status = models.CharField(max_length=100, 
                choices=[('pending', 'Pending'), ('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered')])

    def __str__(self):
        return f"Order #{self.order_id} by {self.customer}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product}"