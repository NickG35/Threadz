import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Product, Watchlist
from users.models import Profile
from orders.models import CartItem
from django.db import transaction
from .forms import ProductForm
from django.contrib import messages
import json
from django.http import JsonResponse
from django.db.models import F, Sum
from django.utils.timezone import now
# Create your views here.

def fetch_products():
    men_url = "https://fakestoreapi.com/products/category/men's%20clothing"
    women_url = "https://fakestoreapi.com/products/category/women's%20clothing"
    #initialize all product list
    all_products = []

    try:
        #fetch men's clothing
        men_response = requests.get(men_url)
        men_products = men_response.json()

        #fetch women's clothing
        women_response = requests.get(women_url)
        women_products = women_response.json()

        #add both gender clothing to all product list
        all_products = men_products + women_products

        #ensures all data is inserted into database
        with transaction.atomic():
            #loop through products and insert fields into database
            for product in all_products:
                Product.objects.get_or_create(
                    name=product['title'],
                    defaults={
                        'price': product['price'],
                        'category': product['category'],
                        'description': product['description'],
                        'image': product['image'],
                    },
                )
    #if there is a fetch error, return an empty list of products with error
    except requests.exceptions.RequestException as e:
        print(f"API fetch error: {e}")
        all_products = []

def index(request):
    existing_products = Product.objects.all()
    #if no products in database, then run the fetch function
    if not existing_products.exists():
        fetch_products()
    
    products = Product.objects.order_by('-creation_time').all()
    user_watchlist  = []
    if request.user.is_authenticated:
        user_watchlist = request.user.profile.watchlist.values_list('product_id', flat=True)

    #pass fetched products to index page
    return render(request, 'index.html', {
        'products': products,
        'user_watchlist': user_watchlist
    })

def product_view(request, product_id):
    user_watchlist = []
    if request.user.is_authenticated:
        user_watchlist = list(request.user.profile.watchlist.values_list('product_id', flat=True))
    product_details = Product.objects.filter(id=product_id).all()

    return render(request, 'product.html', {
        'product_details': product_details,
        'user_watchlist': user_watchlist
    })

def add_to_cart(request, product_id):
    if request.method == 'POST':
        size_choice = request.POST.get('size')

        if not size_choice:
            return JsonResponse({"message": "Pick a size.", "status": "failure"})
        
        product = get_object_or_404(Product, id=product_id)
        
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            user=request.user.profile,
            size=size_choice,
            pending_order=True,
        )

        if not created:
            cart_item.quantity += 1 
            cart_item.save()

        cart_items = CartItem.objects.filter(user=request.user.profile, pending_order=True).order_by('-updated_time')
        cart_total = cart_items.aggregate(total=Sum(F('product__price') * F('quantity')))['total'] or 0
        cart_count = cart_items.aggregate(total_count=Sum('quantity'))['total_count'] or 0

        for item in cart_items:
            print(item.product.name, item.size, item.quantity, item.updated_time)

        cart_item_data = {
            "id": cart_item.id,
            "quantity": cart_item.quantity,
            "size": cart_item.size,
            "cart_total": cart_total,
            "cart_count": cart_count,
            "updated_time": cart_item.updated_time,
            "product": {
                "id": cart_item.product.id,
                "name": cart_item.product.name,
                "price": float(cart_item.product.price),  # Ensure it's serializable
                "image": cart_item.product.image.url if hasattr(cart_item.product.image, 'url') else cart_item.product.image,
                "created_by": cart_item.product.created_by.id if cart_item.product.created_by else None,
            }
        }

        return JsonResponse({
            "message": "Item added to cart.", 
            "status": "success",
            "cart_item": cart_item_data,
        })

    


def create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user.profile
            product.save()
            messages.success(request, 'Product created successfully!')
            return redirect('create')
    else:
        form = ProductForm()
        print(form.errors)
    
    return render(request, 'create.html', {
        'form': form
    })

def toggle_watchlist(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        data = json.loads(request.body)
        status = data.get("status")

        if status == "watched":
            Watchlist.objects.get_or_create(user=request.user.profile, product=product)
            return JsonResponse({"message": "product added to wishlist.", "status": "watched"})
        else:
            Watchlist.objects.filter(user=request.user.profile, product=product).delete()
            return JsonResponse({"message": "removed from wishlist.", "status": "watch"})

def remove_item(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        Watchlist.objects.filter(user=request.user.profile, product=product).delete()
        return JsonResponse({"message": "removed from wishlist."})
           
    

def watchlist_page(request, profile_id):
    profile = Profile.objects.get(user=profile_id)
    watchlist_items = Watchlist.objects.filter(user=profile).order_by('-added_time').all()
    return render(request, "watchlist.html", {
        'watchlist_items': watchlist_items
    })