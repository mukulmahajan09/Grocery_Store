# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import models

from cart.views import _cart_id
from .models import Product, ProductCategory, ProductGallery
from cart.models import CartItem
from django.db.models import Q


def product_display(request, category_slug=None):
    products = None
    categories = None

    if category_slug != None:
        categories = get_object_or_404(ProductCategory, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }

    return render(request, 'index.html', context)

def product_details(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    
    # Get the product gallery
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context = {
        'single_product': single_product,
        'product_gallery': product_gallery,
        'in_cart': in_cart,
    }

    return render(request, 'product-details.html', context)