import requests
from django.shortcuts import render

# Create your views here.
def index(request):
    #fetch api url data
    try:
        url = "https://asos2.p.rapidapi.com/categories/list"
        querystring = {"country":"US","lang":"en-US"}
        headers = {
            "x-rapidapi-key": "f6875f623cmsh6831be6ced70d87p192f91jsnaf20a3d3d5e4",
            "x-rapidapi-host": "asos2.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        products = response.json()

    #if there is a fetch error, return an empty list of products with error
    except requests.exceptions.RequestException as e:
        print(f"API fetch error: {e}")
        products = []

    #pass fetched products to index page
    return render(request, 'index.html', {
        'products': products
    })