from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100, null=False)
    image = models.ImageField(upload_to='product_images/', null=False)
    price = models.IntegerField(null=False)
    description = models.CharField(max_length=300, null=False)
    category = models.CharField(max_length=100, null=False)
