from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product, ProductCategory
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import get_user_model

Account = get_user_model()

# Create your views here.
def display_cart(request, total=0, quantity=0, cart_items=None):
    if request.user.is_authenticated:
        # For authenticated users, get their cart items based on the user
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    else:
        # For anonymous users, get their cart items based on session ID
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
    for cart_item in cart_items:
        total += (cart_item.product.discounted_price * cart_item.quantity)
        quantity += (cart_item.quantity)
    tax = (2 * total)/100
    grand_total = total + tax

    context = {
        'total': total,
        'quantity': quantity,    
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'cart/cart.html', context)

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    current_user = request.user

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )

    if isinstance(current_user, Account):
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart, user=current_user)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
                user=current_user,
            )
    else:
        # For anonymous users, don't assign a user to the cart item
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart, user=None)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
                user=None,
            )

    return redirect('display_cart')

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

    return redirect('display_cart')

def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()

    return redirect('display_cart')


def checkout(request):
    pass