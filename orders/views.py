from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from foods.models import Food
from .models import Cart, CartItem, Order, OrderItem
from .utils import get_cart
from django.conf import settings

from django.http import JsonResponse

def add_to_cart(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    cart = get_cart(request)
    quantity = int(request.POST.get('quantity', 1))
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, food=food)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()
    
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
            item.quantity += 1
            item.save()
        elif action == 'decrease':
            item.quantity -= 1
            if item.quantity <= 0:
                item.delete()
            else:
                item.save()
        elif action == 'remove':
            item.delete()
            
    return redirect('cart_view')

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
        
        if not address or not lat or not lng:
             messages.error(request, "Please provide a valid delivery address.")
             return render(request, 'orders/checkout.html', {'cart': cart, 'google_maps_key': settings.GOOGLE_MAPS_API_KEY})

        order = Order.objects.create(
            user=request.user,
            total_price=cart.total_price,
            delivery_address=address,
            lat=lat,
            lng=lng,
            status='PENDING'
        )
        
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                food=item.food,
                quantity=item.quantity,
                price_at_order=item.food.price
            )
            
        cart.items.all().delete() # Clear cart
        messages.success(request, "Order placed successfully!")
        return redirect('order_history')
        
    return render(request, 'orders/checkout.html', {'cart': cart, 'google_maps_key': settings.GOOGLE_MAPS_API_KEY})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})
