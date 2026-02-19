from .utils import get_cart

def cart_count(request):
    cart = get_cart(request)
    count = sum(item.quantity for item in cart.items.all())
    return {'cart_count': count}
