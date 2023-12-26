from django.db import models
from accounts.models import Account
from store_app.models import Product

# Create your models here.
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Account, on_delete=models.PROTECT)
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