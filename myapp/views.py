from django.shortcuts import render

# Create your views here.
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import Product, InstagramImage


def home(request):
    products = Product.objects.all()
    instagram_images = InstagramImage.objects.all()[:9]  # Limit to 9 images
    return render(request, 'home.html', {
        'products': products,
        'instagram_images': instagram_images
    })

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': product.name,
                        },
                        'unit_amount': int(product.price * 100),  # Convert to cents
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='http://localhost:8000/success/',
                cancel_url='http://localhost:8000/cancel/',
            )
            return redirect(checkout_session.url, code=303)

        except Exception as e:
            return JsonResponse({'error': str(e)})

    return render(request, 'checkout.html', {'product': product})

# myapp/views.py
def success(request):
    return render(request, 'success.html')

def cancel(request):
    return render(request, 'cancel.html')

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})
@login_required
def add_product(request):
    if request.user.is_superuser:  # Allow only the creator/admin
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('home')  # Redirect to homepage after adding product
        else:
            form = ProductForm()
        return render(request, 'add_product.html', {'form': form})
    else:
        return redirect('home')