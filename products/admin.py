from django.contrib import admin
from .models import Product, ProductCategory, ProductGallery
import admin_thumbnails

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug', 'category_desc')
    prepopulated_fields = {'slug': ('category_name',)}

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','category','price','is_available','stock_quantity','created_date','modified_date')
    prepopulated_fields = {'slug': ('product_name',)}

@admin_thumbnails.thumbnail('product_images')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory, CategoryAdmin)