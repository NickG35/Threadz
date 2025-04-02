from .models import CartItem
from django.db.models import Sum, F

def cart_context(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user.profile, pending_order=True).order_by('-updated_time').all()
        cart_total = cart_items.aggregate(total=Sum(F('product__price') * F('quantity')))['total'] or 0
        cart_count = cart_items.aggregate(total_count=Sum('quantity'))['total_count'] or 0
    else:
        cart_items = []
        cart_total = 0
        cart_count = 0
    
    return {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_count': cart_count,
    }
      