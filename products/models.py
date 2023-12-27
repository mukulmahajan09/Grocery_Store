from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
# Create your models here.

class ProductCategory(models.Model):
    category_name = models.CharField(max_length=250, blank=False, null=False)
    slug = models.SlugField(max_length=500, unique=True)
    category_desc = models.TextField(blank=True)
    category_image = models.ImageField(upload_to='products_categories/', blank=True)

    class Meta:
        verbose_name = 'ProductCategory'
        verbose_name_plural = 'Product Categories'

    def slug_url(self):
        return reverse("products_by_category", args=[self.slug])

    def __str__(self):
        return self.category_name
    
class Product(models.Model):
    product_name = models.CharField(max_length=250, blank=False, null=False)
    slug = models.SlugField(max_length=500, unique=True)
    product_desc = models.TextField(blank=False, null=False)
    product_image = models.ImageField(upload_to='products_images/', blank=False, null=False)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    stock_quantity = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
                       
    def __str__(self):
        return self.product_name
