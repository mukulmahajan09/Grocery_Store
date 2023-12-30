from django.db import models
from products.models import Product
from accounts.models import Account

# Create your models here.
class Cart(models.Model):
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)
    
class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    #variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.discounted_price * self.quantity

    def __unicode__(self):
        return str(self.product)