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
