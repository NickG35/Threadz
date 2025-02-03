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
        for items in cart_items:
            items.order = order
            items.pending_order = False
            items.save()
            
        last_four = card_number[-4:]

        request.session['checkout_data'] = {
            'address': address,
            'city': city,
            'zip': zip,
            'card_number': last_four,
            'purchase_id': order.id
        }
        
        return redirect('receipt')
    
    else:
        return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'cart_total': cart_total
    })

def receipt(request):
    # Retrieve data from session
    checkout_data = request.session.get('checkout_data', None)

    if checkout_data:
        address = checkout_data['address']
        city = checkout_data['city']
        zip = checkout_data['zip']
        card_number = checkout_data['card_number']
        purchase_id = checkout_data['purchase_id']

        del request.session['checkout_data']

        purchase = Order.objects.get(id=purchase_id)

        return render(request, 'receipt.html', {
            'address': address,
            'city': city,
            'zip': zip, 
            'card_number': card_number,
            'purchase': purchase
        })
    else:
        return redirect('checkout')