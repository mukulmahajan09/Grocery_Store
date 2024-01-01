from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
        for cart_item in cart_items:
            total += (cart_item.product.discounted_price * cart_item.quantity)
            quantity += (cart_item.quantity)

    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
    }

    return render(request, 'cart.html', context)

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id): #1

    product = get_object_or_404(Product, pk=product_id) #1 match

    try:
        if request.user.is_authenticated: 
           cart_item = CartItem.objects.get_or_create(user=request.user) 
        else:
            # user is not authenticated, in this we can rely on the session id
            cart = Cart.objects.get_or_create(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get_or_create(product=product, cart=cart) 
 
        cart_item.quantity += 1
        cart_item.save()
    
    except:
        pass

    return redirect('cart')

def remove_cart(request, product_id, cart_item_id):

    product = get_object_or_404(Product, id=product_id)

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            # user is not authenticated, in this we can rely on the session id
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    
    except:
        pass

    return redirect('cart')

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