from django.db import models
from products.models import Product
from users.models import Profile

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField()

    def __str__(self):
        return f"order number: {self.id}"
    
class CartItem(models.Model):
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Extra Extra Large'),
    ]
     
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    size = models.CharField(max_length=3, choices=SIZE_CHOICES, default='M')
    quantity = models.IntegerField(default=1)
    stow_date = models.DateTimeField(auto_now_add=True)
    pending_order = models.BooleanField(default=True)
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE, related_name='cart_item')

    def __str__(self):
        return f"{self.product}"