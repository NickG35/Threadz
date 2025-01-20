import requests
from django.shortcuts import render

# Create your views here.
def index(request):
    #fetch api url data
    api_url = 'https://fakestoreapi.com/products'
    try:
        response = requests.get(api_url)
        products = response.json()
    #if there is a fetch error, return an empty list of products with error
    except requests.exceptions.RequestException as e:
        print(f"API fetch error: {e}")
        products = []

    #pass fetched products to index page
    return render(request, 'index.html', {
        'products': products
    })