from django.shortcuts import render, redirect
from .models import CartItem, Order
from django.db.models import F, Sum
from .forms import CheckoutForm

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
        form = CheckoutForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zip_code = form.cleaned_data['zip']
            card_number = form.cleaned_data['card_number']

            order = Order.objects.create(
                user=request.user.profile,
                total_price = cart_total
            )
            
            last_four = card_number[-4:]

            for item in cart_items:
                item.pending_order=False
                item.order = order
                item.save()


            request.session['checkout_data'] = {
                'first_name': first_name,
                'last_name': last_name,
                'address': address,
                'city': city,
                'state': state,
                'zip': zip_code,
                'card_number': last_four,
                'purchase_id': order.id
            }
        
            return redirect('receipt')
    
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'form': form
    })

def receipt(request):
    # Retrieve data from session
    checkout_data = request.session.get('checkout_data', None)

    if checkout_data:
        first_name = checkout_data['first_name']
        last_name = checkout_data['last_name']
        address = checkout_data['address']
        city = checkout_data['city']
        state = checkout_data['state']
        zip_code = checkout_data['zip']
        card_number = checkout_data['card_number']
        purchase_id = checkout_data['purchase_id']

        del request.session['checkout_data']

        purchase = Order.objects.get(id=purchase_id)

        return render(request, 'receipt.html', {
            'first_name': first_name,
            'last_name': last_name,
            'address': address,
            'city': city,
            'state': state,
            'zip_code': zip_code, 
            'card_number': card_number,
            'purchase': purchase
        })
    else:
        return render(request, 'receipt.html')

def order_details(request, order_id):
    order_details = Order.objects.get(id=order_id)
    return render(request, 'orders.html', {
        'order_details': order_details
    })