from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from foods.models import Food
from .models import Cart, CartItem, Order, OrderItem
from .utils import get_cart
from django.conf import settings
from django.db import transaction

from django.http import JsonResponse

def add_to_cart(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    cart = get_cart(request)
    quantity = int(request.POST.get('quantity', 1))
    
    # Stock check
    cart_item = CartItem.objects.filter(cart=cart, food=food).first()
    current_qty = cart_item.quantity if cart_item else 0
    new_qty = current_qty + quantity
    
    if new_qty > food.stock:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'message': f"Only {food.stock} units of {food.name} are available."
            }, status=400)
        messages.error(request, f"Only {food.stock} units of {food.name} are available.")
        return redirect('food_detail', slug=food.slug)

    if cart_item:
        cart_item.quantity = new_qty
        cart_item.save()
    else:
        CartItem.objects.create(cart=cart, food=food, quantity=quantity)
    
    total_items = sum(item.quantity for item in cart.items.all())
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': f"{food.name} added to cart.",
            'cart_count': total_items
        })
    
    messages.success(request, f"{food.name} added to cart.")
    return redirect('food_detail', slug=food.slug)

def cart_view(request):
    cart = get_cart(request)
    return render(request, 'orders/cart.html', {'cart': cart})

def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    # Ensure user owns this cart item
    cart = get_cart(request)
    if item.cart != cart:
        return redirect('cart_view')
        
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            if item.quantity + 1 > item.food.stock:
                messages.error(request, f"Only {item.food.stock} units of {item.food.name} are available.")
            else:
                item.quantity += 1
                item.save()
                messages.success(request, f"Increased quantity of {item.food.name}.")
        elif action == 'decrease':
            item.quantity -= 1
            if item.quantity <= 0:
                name = item.food.name
                item.delete()
                messages.success(request, f"Removed {name} from cart.")
            else:
                item.save()
                messages.success(request, f"Decreased quantity of {item.food.name}.")
        elif action == 'remove':
            name = item.food.name
            item.delete()
            messages.success(request, f"Removed {name} from cart.")
            
    return redirect('cart_view')

import requests
import json
from django.urls import reverse

@login_required
def checkout(request):
    cart = get_cart(request)
    if not cart.items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('food_list')
        
    if request.method == 'POST':
        address = request.POST.get('address')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        payment_method = request.POST.get('payment_method')
        
        if not address or not lat or not lng:
             messages.error(request, "Please provide a valid delivery address.")
             return render(request, 'orders/checkout.html', {'cart': cart, 'google_maps_key': settings.GOOGLE_MAPS_API_KEY})
        
        if not payment_method:
            messages.error(request, "Please select a payment method.")
            return render(request, 'orders/checkout.html', {'cart': cart, 'google_maps_key': settings.GOOGLE_MAPS_API_KEY})

        # Final stock check before order
        for item in cart.items.all():
            if item.quantity > item.food.stock:
                messages.error(request, f"Sorry, {item.food.name} is now out of stock or insufficient (Available: {item.food.stock}).")
                return redirect('cart_view')

        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                total_price=cart.total_price,
                delivery_address=address,
                lat=lat,
                lng=lng,
                status='PENDING',
                payment_method=payment_method,
                payment_status='PENDING'
            )
            
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    food=item.food,
                    quantity=item.quantity,
                    price_at_order=item.food.price
                )
                # Deduct stock
                item.food.stock -= item.quantity
                item.food.save()
                
            if payment_method == 'KHALTI':
                # Khalti Payment Initiation
                url = "https://dev.khalti.com/api/v2/epayment/initiate/"
                return_url = request.build_absolute_uri(reverse('khalti_verify'))
                
                payload = json.dumps({
                    "return_url": return_url,
                    "website_url": request.build_absolute_uri(reverse('home')),
                    "amount": int(float(order.total_price) * 100), # amount in paisa
                    "purchase_order_id": str(order.id),
                    "purchase_order_name": f"Order #{order.id} - {request.user.username}",
                    "customer_info": {
                        "name": request.user.get_full_name() or request.user.username,
                        "email": request.user.email,
                        "phone": request.user.phone or "9800000000" # fallback if phone not set
                    }
                })
                
                headers = {
                    'Authorization': f'key {settings.KHALTI_SECRET_KEY}',
                    'Content-Type': 'application/json',
                }

                try:
                    response = requests.post(url, headers=headers, data=payload)
                    response_data = response.json()
                    
                    if 'pidx' in response_data:
                        order.khalti_pidx = response_data['pidx']
                        order.save()
                        return redirect(response_data['payment_url'])
                    else:
                        raise Exception(f"Khalti initiation failed: {response_data.get('detail', 'Unknown error')}")
                except Exception as e:
                    messages.error(request, str(e))
                    transaction.set_rollback(True)
                    return redirect('checkout')
                    
            # For COD and others
            cart.items.all().delete() # Clear cart
            messages.success(request, "Order placed successfully!")
            return redirect('order_history')
        
    return render(request, 'orders/checkout.html', {'cart': cart, 'google_maps_key': settings.GOOGLE_MAPS_API_KEY})

@login_required
def khalti_verify(request):
    pidx = request.GET.get('pidx')
    purchase_order_id = request.GET.get('purchase_order_id')
    transaction_id = request.GET.get('transaction_id')
    
    if not pidx:
        messages.error(request, "Invalid payment identifier (pidx).")
        return redirect('order_history')
        
    url = "https://dev.khalti.com/api/v2/epayment/lookup/"
    payload = json.dumps({"pidx": pidx})
    headers = {
        'Authorization': f'key {settings.KHALTI_SECRET_KEY}',
        'Content-Type': 'application/json',
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        response_data = response.json()
        
        if response_data.get('status') == 'Completed':
            order = get_object_or_404(Order, id=purchase_order_id, khalti_pidx=pidx)
            order.payment_status = 'PAID'
            order.transaction_id = transaction_id
            order.save()
            
            # Clear user cart on successful payment
            cart = get_cart(request)
            cart.items.all().delete()
            
            messages.success(request, f"Payment successful for Order #{order.id}!")
            return redirect('order_history')
        else:
            messages.error(request, f"Khalti payment not completed. Status: {response_data.get('status')}")
            return redirect('order_history')
            
    except Exception as e:
        messages.error(request, f"Payment verification error: {str(e)}")
        return redirect('order_history')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status == 'PENDING':
        with transaction.atomic():
            order.status = 'CANCELLED'
            order.save()
            
            # Restore stock
            for item in order.items.all():
                item.food.stock += item.quantity
                item.food.save()
                
            messages.success(request, f"Order #{order.id} has been cancelled and stock restored.")
    else:
        messages.error(request, f"Order #{order.id} cannot be cancelled as it is already {order.get_status_display().lower()}.")
        
    return redirect('order_history')
