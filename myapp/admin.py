from django.contrib import admin
from .models import Product, Category, Brand

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'size', 'price', 'created_at')
    list_filter = ('category', 'brand', 'size')
    search_fields = ('name', 'description')

admin.site.register(Category)
admin.site.register(Brand)