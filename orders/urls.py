from django.urls import path

from . import views

urlpatterns = [
    path("cart", views.cart, name="cart"),
    path("delete_item/<int:product_id>", views.delete_item, name="delete_item"),
    path("checkout", views.checkout, name="checkout"),
    path("receipt/<int:purchase_id>", views.receipt, name="receipt"),
    path("order_details/<int:order_id>", views.order_details, name="order_details")
]