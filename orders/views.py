from django.shortcuts import render, redirect
from .models import CartItem, Order
from django.db.models import F, Sum
from .forms import CheckoutForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

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

def delete_item(request, product_id):
    if request.method == 'POST':
        cart_item = CartItem.objects.get(product=product_id, user=request.user.profile)
        cart_item.delete()
        return JsonResponse({"message": "Cart item deleted.", "status": "success"})

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

            last_four = card_number[-4:]

            order = Order.objects.create(
                user=request.user.profile,
                total_price = cart_total,
                first_name = first_name,
                last_name = last_name,
                address = address,
                city = city,
                state = state,
                zip_code = zip_code,
                card_number = last_four,
            )

            for item in cart_items:
                item.pending_order=False
                item.order = order
                item.save()
        
            return redirect('receipt', purchase_id=order.id)
    
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'form': form
    })

def receipt(request, purchase_id):
    purchase = Order.objects.get(id=purchase_id)
    return render(request, 'receipt.html', {
        'purchase': purchase
    })

def order_details(request, order_id):
    order_details = Order.objects.get(id=order_id)
    return render(request, 'orders.html', {
        'order_details': order_details
    })