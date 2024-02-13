from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from cart.models import Cart, CartItem
from .models import Order, Payment, OrderProduct
from accounts.models import UserProfile, UserAddress
from products.models import Product
from .forms import OrderForm, NewUserAddress
import datetime
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Create your views here.
def place_order(request):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    count = cart_items.count()
    if count <= 0:
        return redirect('store')
    
    grand_total = 0
    tax = 0
    total = 0
    quantity = 0

    for cart_item in cart_items:
        total += (cart_item.product.discounted_price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        address_form = NewUserAddress(request.POST)
        if order_form.is_valid() and address_form.is_valid():

            # Retrieve the UserProfile instance for the current_user
            user_profile = UserProfile.objects.get(user=current_user)

            # Process the order form data
            order = Order.objects.create(
                user=current_user,
                order_note=order_form.cleaned_data['order_note'],
                total_order_amount=grand_total,
                tax=tax,
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            # Process the address form data
            address = UserAddress.objects.create(
                    user_address=user_profile,
                    full_name=address_form.cleaned_data['full_name'],
                    phone_number=address_form.cleaned_data['phone_number'],
                    email=address_form.cleaned_data['email'],
                    address_line_1=address_form.cleaned_data['address_line_1'],
                    address_line_2=address_form.cleaned_data['address_line_2'],
                    pincode=address_form.cleaned_data['pincode'],
                    city=address_form.cleaned_data['city'],
                    state=address_form.cleaned_data['state'],
                    country=address_form.cleaned_data['country']
            )

            # Assign the address to the order
            order.shipping_address = address
            order.save()

            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(order.id)
            order.order_number = order_number
            order.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payment.html', context)
    else:
        return redirect('checkout')


def payment(request):
    body = json.loads(request.body)

    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderId'])

    # Store transaction details inside Payment model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        total_order_amount_paid = order.order_total,
        payment_status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move the cart items to Order Product table
    cart_items = CartItem.objects.filter(user=request.user)

    for cart_item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.user_id = request.user.id
        orderproduct.order_id = order.id 
        orderproduct.product_id = cart_item.product_id
        orderproduct.payment = payment
        orderproduct.product_price = cart_item.product.discounted_price
        orderproduct.quantity = cart_item.quantity
        orderproduct.ordered = True
        orderproduct.save()

        # Reduce the quantity of the sold products
        product = Product.objects.get(id=cart_item.product_id)
        product.stock_quantity -= cart_item.quantity
        product.save()

    # Clear cart
    CartItem.objects.filter(user=request.user).delete()

    # Send order recieved email to customer
    mail_subject = 'Thank you for your order!'
    message = render_to_string('orders/order_recieved_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    # Send order number and transaction id back to sendData method via JsonResponse
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)
    

def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')