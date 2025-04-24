from django.shortcuts import render

# Create your views here.
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import Product, InstagramImage
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import stripe
from .models import Product
from django.conf import settings

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = 'whsec_a9f54b6d4b976fcc0ca9be5a5ccf7cb733a3ea32de925ed5bfc81c7f3116cbb9'  # You'll replace this in step 4

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        product_ids = session.get('metadata', {}).get('product_ids', '')
        print("🧾 Product IDs from metadata:", product_ids)

        for product_id in product_ids.split(','):
            if product_id.isdigit():
                deleted, _ = Product.objects.filter(id=product_id).delete()
                print(f"🗑️ Deleted product {product_id}: {deleted} row(s)")

    return HttpResponse(status=200)

def home(request):
    products = Product.objects.all()
    instagram_images = InstagramImage.objects.all()[:9]  # Limit to 9 images
    return render(request, 'home.html', {
        'products': products,
        'instagram_images': instagram_images
    })

from .models import Product  # or wherever your Product model is

def cart(request):
    cart = request.session.get('cart', {})  # { '3': 1, '5': 2 }

    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            item_total = product.price * quantity
            total_price += item_total

            cart_items.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'quantity': quantity,
                'image': product.images.first().image.url if product.images.exists() else '',
            })
        except Product.DoesNotExist:
            continue

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

stripe.api_key = settings.STRIPE_SECRET_KEY

from django.shortcuts import redirect

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 1)  # Default quantity = 1
    request.session['cart'] = cart
    return redirect('product_detail', product_id=product_id)

def remove_from_cart(request, item_id):
    # Logic to remove the item from the cart
    # If you're using session-based cart:
    cart = request.session.get('cart', {})

    # Remove item from session cart dict
    cart.pop(str(item_id), None)

    request.session['cart'] = cart
    return redirect('cart')


def cart_checkout(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        line_items = []

        for product_id, quantity in cart.items():
            try:
                product = Product.objects.get(id=product_id)
                line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(product.price * 100),
                        'product_data': {
                            'name': product.name,
                        },
                    },
                    'quantity': quantity,
                })
            except Product.DoesNotExist:
                continue

        if not line_items:
            return redirect('cart')  # Nothing to checkout

        session_data = {
            'payment_method_types': ['card'],
            'line_items': line_items,
            'mode': 'payment',
            'success_url': 'http://127.0.0.1:8000/success/',
            'cancel_url': 'http://127.0.0.1:8000/cart/',
            'shipping_address_collection': {
                'allowed_countries': ['US']
            },
            'billing_address_collection': 'required',
            'metadata': {
                'product_ids': ','.join(cart.keys())  # ✅ moved metadata here
            }
        }

        if request.user.is_authenticated and request.user.email:
            session_data['customer_email'] = request.user.email

        checkout_session = stripe.checkout.Session.create(**session_data)
        return redirect(checkout_session.url, code=303)

    # ✅ If not POST, just redirect to cart
    return redirect('cart')


# myapp/views.py
def success(request):
    request.session['cart'] = {}
    return render(request, 'success.html')

def cancel(request):
    return render(request, 'cancel.html')

def terms(request):
    return render(request, 'terms.html')

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    return render(request, 'product_detail.html', {
        'product': product,
        'cart': cart,
    })

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