from django.shortcuts import render, get_object_or_404

from .models import Category, Product
# Create your views here.


def all_products(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'products/home.html', context)

def product_detail(request, slug):
    obj = get_object_or_404(Product, slug=slug)
    context = {
        'products': [obj]
    }
    return render(request, 'products/home.html', context)