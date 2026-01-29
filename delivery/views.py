from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from orders.models import Order
from django.conf import settings

@login_required
def dashboard(request):
    if request.user.role != 'DELIVERY_BOY':
        messages.error(request, "Access denied.")
        return redirect('home')
        
    # Orders assigned to this delivery boy
    assigned_orders = Order.objects.filter(delivery_boy=request.user).exclude(status='COMPLETED').order_by('-created_at')
    
    # Available orders (Pending and not assigned) - simplistic logic for now
    available_orders = Order.objects.filter(status='PENDING', delivery_boy__isnull=True).order_by('-created_at')
    
    completed_orders = Order.objects.filter(delivery_boy=request.user, status='COMPLETED').order_by('-created_at')[:10]
    
    return render(request, 'delivery/dashboard.html', {
        'assigned_orders': assigned_orders,
        'available_orders': available_orders,
        'completed_orders': completed_orders,
        'google_maps_key': settings.GOOGLE_MAPS_API_KEY
    })

@login_required
def accept_order(request, order_id):
    if request.user.role != 'DELIVERY_BOY':
        return redirect('home')
        
    order = get_object_or_404(Order, id=order_id)
    if order.delivery_boy is None:
        order.delivery_boy = request.user
        order.status = 'ACCEPTED'
        order.save()
        messages.success(request, f"Order #{order.id} accepted.")
    
    return redirect('delivery_dashboard')

@login_required
def update_status(request, order_id):
    if request.user.role != 'DELIVERY_BOY':
        return redirect('home')
        
    order = get_object_or_404(Order, id=order_id)
    if order.delivery_boy != request.user:
        return redirect('delivery_dashboard')
        
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['ON_THE_WAY', 'COMPLETED']:
            order.status = new_status
            order.save()
            messages.success(request, f"Order #{order.id} status updated to {new_status}.")
            
    return redirect('delivery_dashboard')
