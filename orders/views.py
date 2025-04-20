from django.shortcuts import render, redirect
from .models import CartItem, Order
from django.db.models import F, Sum
from .forms import CheckoutForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json

# Create your views here.
def cart(request):
    if request.method == 'POST':
        return redirect('checkout')
    
    else:
        cart_items = CartItem.objects.filter(user=request.user.profile, pending_order=True).order_by('-updated_time').all()
        cart_total = cart_items.aggregate(total=Sum(F('product__price') * F('quantity')))['total'] or 0

        return render(request, 'cart.html', {
            'disabled':True,
            'cart_items': cart_items,
            'cart_total': cart_total,
        })

def delete_item(request, product_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        size = data.get('size')

        if not size:
            return JsonResponse({"message": "Failed to delete cart item.", "status": "failure"})

        cart_items = CartItem.objects.filter(product=product_id, size=size, user=request.user.profile, pending_order=True)
        cart_items.delete()

        cart_item = CartItem.objects.filter(user=request.user.profile, pending_order=True)
        cart_total = cart_item.aggregate(total=Sum(F('product__price') * F('quantity')))['total'] or 0
        cart_count = cart_item.aggregate(total_count=Sum('quantity'))['total_count'] or 0
        
        return JsonResponse({"message": "Cart item deleted.", "status": "success", "cart_total": cart_total, "cart_count": cart_count})

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
        'disabled':True,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'form': form
    })

def receipt(request, purchase_id):
    purchase = Order.objects.get(id=purchase_id)
    return render(request, 'receipt.html', {
        'disabled':True,
        'purchase': purchase
    })

def order_details(request, order_id):
    order_details = Order.objects.get(id=order_id)
    return render(request, 'orders.html', {
        'order_details': order_details,
         "hidden": True
    })