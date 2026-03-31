from .models import Cart, CartItem

def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key, user=None)
    return cart

def merge_cart(request, user, guest_session_key=None):
    if not guest_session_key:
        guest_session_key = request.session.session_key
        
    if not guest_session_key:
        return
        
    try:
        # Find car exactly by session_key and ensure user is None (guest cart)
        guest_cart = Cart.objects.get(session_key=guest_session_key, user=None)
    except Cart.DoesNotExist:
        return

    user_cart, created = Cart.objects.get_or_create(user=user)

    for item in guest_cart.items.all():
        user_item, created = CartItem.objects.get_or_create(cart=user_cart, food=item.food)
        if not created:
            user_item.quantity += item.quantity
            user_item.save()
        else:
            user_item.quantity = item.quantity
            user_item.save()
    
    # After merging, we should clear the items and the guest cart
    guest_cart.delete()
