from django.shortcuts import render
from .models import CartItem

# Create your views here.
def orders(request):
    cart_items = CartItem.objects.filter(user=request.user.profile).order_by('-stow_date').all()
    return render(request, 'orders.html', {
        'cart_items': cart_items
    })