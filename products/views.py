from django.shortcuts import render, get_object_or_404

from .models import Category, Product
from .forms import ProductCreateForm
# Create your views here.


def all_products(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'home.html', context)

def product_detail(request, id):
    #product = get_object_or_404(Product, slug=slug)
    product = get_object_or_404(Product, id=id)
    context = {
        'product_details': product
    }
    return render(request, 'products/product_details.html', context)

def product_create(request):
    create_form = ProductCreateForm(request.POST or None, request.FILES)
    if create_form:
        print("if create_form is there ")
    if create_form.is_valid():
        print("inside is valid")
        create_form.save()
        print("fomr saved")
        create_form = ProductCreateForm()
    else:
        print(create_form.errors.__dict__)
    context = {
        'create_form':create_form
    }

    return render(request,'products/product_create.html', context)

def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    print (products)
    context = {
        'category': category,
        'products': products,
    }
    return  render(request, 'products/category.html', context=context)