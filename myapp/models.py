from django.db import models

# Create your models here.
from django.db import models

# Categories
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Brands
class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Product Model
class Product(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name