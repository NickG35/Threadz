from django.db import models
from users.models import Profile

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100, null=False)
    image = models.ImageField(upload_to='product_images/', null=False)
    price = models.IntegerField(null=False)
    description = models.CharField(max_length=300, null=False)
    CATEGORY_CHOICES = [
        ("", "Select a category"),
        ("men's clothing", "Men's Clothing"),
        ("women's clothing","Women's Clothing"),
    ]
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, null=False)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True, related_name='products')

    def __str__(self):
        return f"{self.name}"
