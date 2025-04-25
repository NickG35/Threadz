from django.db import models
from products.models import Product
from users.models import Profile
from django.utils.timezone import now

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    purchase_date = models.DateField(auto_now_add=True)
    total_price = models.IntegerField()
    address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=100, null=True)
    zip_code = models.CharField(max_length=10, null=True)
    card_number = models.IntegerField(null=True)

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
    updated_time = models.DateTimeField(auto_now=True)
    pending_order = models.BooleanField(default=True)
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE, related_name='cart_item')

    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_time = now()  # Update timestamp when saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product}"
    
