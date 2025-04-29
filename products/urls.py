from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("filter/<str:category>", views.filter_products, name='filter'),
    path("product/<int:product_id>", views.product_view, name="product"),
    path("product/add/<int:product_id>", views.add_to_cart, name="add_to_cart"),
    path("product/create", views.create, name="create"),
    path("<int:product_id>", views.toggle_watchlist, name='toggle_watch'),
    path("remove_item/<int:product_id>", views.remove_item, name='remove_item'),
    path("watchlist/<int:profile_id>", views.watchlist_page, name='watchlist')
]