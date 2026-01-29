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

def merge_cart(request, user):
    session_key = request.session.session_key
    if not session_key:
        return
        
    try:
        guest_cart = Cart.objects.get(session_key=session_key, user=None)
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
    
    guest_cart.delete()
