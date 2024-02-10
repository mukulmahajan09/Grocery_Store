from django.db import models
from accounts.models import Account, UserAddress
from products.models import Product
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100)
    total_order_amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=100, choices=[('pending', 'Pending'), ('paid', 'Paid'), ('failed', 'Failed')])
    created_at = models.DateTimeField(auto_now_add=True)
    

class Order(models.Model):
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    shipping_address = models.ForeignKey(UserAddress, on_delete=models.SET_NULL, null=True)
    order_note = models.CharField(max_length=100, blank=True)
    tax = models.FloatField()
    total_order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=100, 
                choices=[('pending', 'Pending'), ('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered')])
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderProduct(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #variations = models.ManyToManyField(Variation, blank=True)
    
    def __str__(self):
        return self.product.product_name

    def __str__(self):
        return f"{self.quantity} x {self.product}"