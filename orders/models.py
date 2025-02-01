from django.db import models
from products.models import Product
from users.models import Profile

# Create your models here.
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    size = models.CharField(max_length=5)
    quantity = models.IntegerField(default=1)
    stow_date = models.DateTimeField(auto_now_add=True)
    pending_order = models.BooleanField(default=True)

class Order(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    cart_item = models.ManyToManyField(CartItem)
    purchase_date = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField()