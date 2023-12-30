# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import models
from products.models import Product, ProductCategory, ProductGallery

def product_display(request):

    products = Product.objects.all().filter(is_available=True)

    context = {
        'products': products,
    }

    return render(request, 'index.html', context)

def product_details(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    
    # Get the product gallery
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context = {
        'single_product': single_product,
        'product_gallery': product_gallery,
    }

    return render(request, 'product-details.html', context)