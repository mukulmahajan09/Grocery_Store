from django.contrib import admin
from .models import Product, ProductCategory, ProductGallery, ReviewRating
import admin_thumbnails

# Register your models here.
@admin_thumbnails.thumbnail('product_images')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug', 'category_desc')
    prepopulated_fields = {'slug': ('category_name',)}

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','category','original_price','discounted_price','is_available','stock_quantity','created_date','modified_date')
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductGalleryInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory, CategoryAdmin)
admin.site.register(ProductGallery)
admin.site.register(ReviewRating)