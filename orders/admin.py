from django.contrib import admin
from .models import Order, CartItem

# Register your models here.
admin.site.register(Order)

class CartItemAdmin(admin.ModelAdmin):
    # Specify the fields to display in the list view
    list_display = ('product', 'user', 'size', 'quantity', 'stow_date', 'updated_time', 'pending_order')
    
    # Optionally add search and filters
    search_fields = ('product__name', 'user__username')
    list_filter = ('size', 'pending_order')

# Register the model with the custom admin
admin.site.register(CartItem, CartItemAdmin)