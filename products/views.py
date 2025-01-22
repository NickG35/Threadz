import requests
from django.shortcuts import render
from .models import Product
from django.db import transaction

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
    products = Product.objects.all()
    #if no products in database, then run the fetch function
    if not products.exists():
        fetch_products()
        products = Product.objects.all()
    #pass fetched products to index page
    return render(request, 'index.html', {
        'products': products
    })