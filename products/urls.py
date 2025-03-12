from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("product/<int:product_id>", views.product, name="product"),
    path("product/create", views.create, name="create"),
    path("<int:product_id>", views.toggle_watchlist, name='toggle_watch'),
    path("remove_item/<int:product_id>", views.remove_item, name='remove_item'),
    path("watchlist/<int:profile_id>", views.watchlist_page, name='watchlist')
]