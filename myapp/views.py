from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import Product


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})
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