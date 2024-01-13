# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import models
from django.db.models import Q
from products.models import Product, ProductCategory, ProductGallery

def store(request):
    products = Product.objects.all().filter(is_available=True)
    product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.filter(Q(product_name__icontains=keyword) | Q(product_desc__icontains=keyword))
            product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)