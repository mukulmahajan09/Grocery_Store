from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from accounts.models import Account
from django.db.models import Avg, Count

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
    #product_short_desc = models.TextField(blank=False, null=False)
    product_desc = models.TextField(blank=False, null=False)
    product_image = models.ImageField(upload_to='products_images/', blank=False, null=False)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    stock_quantity = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
                       
    def __str__(self):
        return self.product_name

    def averageReviews(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReviews(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

    
class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    product_images = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'ProductGallery'
        verbose_name_plural = 'ProductGalleries'


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200, blank=False, null=False)
    review = models.TextField(blank=False, null=False)
    rating = models.FloatField()
    ip_address = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject