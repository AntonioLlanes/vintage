from django.contrib import admin
from .models import Product, ProductImage, Category, Brand, InstagramImage
import requests
from bs4 import BeautifulSoup

def get_instagram_image_url(post_url):
    """Retrieve the image URL from an instagram post."""
    try:
        # Send a GET request to the instagram post
        response = requests.get(post_url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()  # Raise an error for bad status codes

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the image tag
        meta_tag = soup.find('meta', property='og:image')
        if meta_tag:
            return meta_tag['content']  # Return the image URL

    except Exception as e:
        print(f"Error retrieving image: {e}")
        return None

# ✅ Inline to allow multiple image uploads directly within the Product admin page
class ProductImageInline(admin.TabularInline):  # Use StackedInline for vertical layout
    model = ProductImage
    extra = 3  # Allows adding up to 3 images at once (adjust as needed)

    @admin.register(InstagramImage)
    class InstagramImageAdmin(admin.ModelAdmin):
        list_display = ['image_file', 'link']

    @admin.action(description='Fetch image URLs for selected posts')
    def fetch_image_urls(self, request, queryset):
        """Admin action to fetch image URLs for selected posts."""
        for obj in queryset:
            if obj.post_url and not obj.image_url:
                obj.image_url = get_instagram_image_url(obj.post_url)
                obj.save()
        self.message_user(request, "Image URLs have been fetched successfully.")
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'price', 'created_at')
    inlines = [ProductImageInline]  # ✅ Add ProductImageInline for multiple image uploads


# Register other models
admin.site.register(Category)
admin.site.register(Brand)
