import requests
from django.shortcuts import render, redirect
from .models import Product
from orders.models import CartItem
from django.db import transaction
from .forms import ProductForm
from django.contrib import messages
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
    #pass fetched products to index page
    return render(request, 'index.html', {
        'products': products
    })

def product(request, product_id):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        request.POST.get('size')
        product_name = Product.objects.get(id=product_id)
        CartItem.objects.create(
            product=product_name,
            user = request.user.profile
        )
        messages.success(request, 'Item added to cart.')
        return redirect('product')
    else:
        product_details = Product.objects.filter(id=product_id).all()
        return render(request, "product.html", {
            'product_details': product_details
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
