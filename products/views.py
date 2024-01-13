# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import models

from cart.views import _cart_id
from .models import Product, ProductCategory, ProductGallery, ReviewRating
from cart.models import CartItem
from django.db.models import Q
from .forms import ReviewForm


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
    
    # Get the reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True).order_by('-created_at')

    # Get the product gallery
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context = {
        'single_product': single_product,
        'product_gallery': product_gallery,
        'in_cart': in_cart,
        'reviews': reviews,
    }

    return render(request, 'products/product-details.html', context)


def review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            review = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=review)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip_address = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)