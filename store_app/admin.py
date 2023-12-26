from django.contrib import admin
from .models import Customer, Product, ProductCategory, Order, OrderItem

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(Order)
admin.site.register(OrderItem)