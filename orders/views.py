from django.shortcuts import render, redirect
from .models import CartItem, Order
from django.db.models import F, Sum

# Create your views here.
def cart(request):
    if request.method == 'POST':
        return redirect('checkout')
    
    else:
        cart_items = CartItem.objects.filter(user=request.user.profile, pending_order=True).order_by('-stow_date').all()
        cart_total = cart_items.aggregate(total=Sum(F('product__price') * F('quantity')))['total'] or 0

        return render(request, 'cart.html', {
            'cart_items': cart_items,
            'cart_total': cart_total
        })

def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user.profile, pending_order=True).order_by('-stow_date').all()
    cart_total = cart_items.aggregate(total=Sum(F('product__price') * F('quantity')))['total'] or 0

    if request.method == 'POST':
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip = request.POST.get('zip')
        card_number = request.POST.get('card_number')
        order = Order.objects.create(
            user=request.user.profile,
            total_price = cart_total
        )
        order.cart_item.add(*cart_items)
        purchase = Order.objects.filter(user=request.user.profile).latest('purchase_date')
        cart_items.update(pending_order=False)
        last_four = card_number[-4:]
        
        return render(request,'receipt.html', {
            'address': address,
            'city': city,
            'zip': zip,
            'card_number': last_four,
            'purchase': purchase
        })
    
    else:
        return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'cart_total': cart_total
    })

def receipt(request):
    return render(request, 'receipt.html')