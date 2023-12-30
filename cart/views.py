from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
def cart(request):
    return render(request, 'cart.html')

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):

    product = get_object_or_404(Product, pk=product_id)

    try:
        if request.user.is_authenticated:
           cart_item = CartItem.objects.get_or_create(user=request.user) 
        else:
            # user is not authenticated, in this we can rely on the session id
            cart_id = _cart_id(request)
            cart = Cart.objects.get_or_create(cart_id=cart_id)
            cart_item = CartItem.objects.get_or_create(product=product, cart=cart_id) 
 
        cart_item.quantity += 1
        cart_item.save()
    
    except:
        pass

    redirect('cart')

def remove_cart(request, product_id, cart_item_id):

    product = get_object_or_404(Product, id=product_id)

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            # user is not authenticated, in this we can rely on the session id
            cart_id = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart_id, id=cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    
    except:
        pass

    redirect('cart')

 #current_user = request.user
    #product = Product.objects.get(id=product_id)
#
    #if current_user.is_authenticated:
    #    if request.method == 'POST':
    #        for item in request.POST:
    #            key = item
    #            value = request.POST[key]
#
    #    is_cart_item_exist = CartItem.objects.filter(product=product, user=current_user).exists()
    #    if is_cart_item_exist:
    #        cart_item = CartItem.objects.filter(product=product, user=current_user)