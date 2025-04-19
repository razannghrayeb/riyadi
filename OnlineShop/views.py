from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Order, OrderItem, User, Payment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Order, OrderItem, User, Payment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required(login_url='/auth/login')
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(user=request.user, complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if not created:
        order_item.quantity += 1
        order_item.save()

    return redirect('cart')

@login_required(login_url='/auth/login')
def remove_from_cart(request, order_item_id):
    order_item = OrderItem.objects.get(id=order_item_id)
    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save()
    else:
        order_item.delete()
    return redirect('cart')

@login_required(login_url='/auth/login')
def cart(request):
    order = Order.objects.get(user=request.user, complete=False)
    order_items = order.orderitem_set.all()
    return render(request, 'football_shop/cart.html', {'order': order, 'order_items': order_items})

@login_required(login_url='/auth/login')
def checkout(request):
    order = Order.objects.get(user=request.user, complete=False)
    if request.method == 'POST':
        # Process payment (you need to implement this part using a payment gateway like Stripe or PayPal)
        payment = Payment.objects.create(user=request.user, amount=order.get_cart_total())
        order.complete = True
        order.save()
        messages.success(request, f'Payment successful! Your order has been placed.')
        return redirect('home')
    return render(request, 'football_shop/checkout.html', {'order': order})



def Shop_Main(request):
    products = Product.objects.all()
    for product in products:
        if product.image:
            product.image_url = product.image.url
        else:
            product.image_url = None  # Or a default placeholder image path
    return render(request, 'OnlineShop/shop.html', {'products': products})