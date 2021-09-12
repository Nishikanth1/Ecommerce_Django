from django.shortcuts import render, get_object_or_404

from .basket import Basket
from products.models import Product
# Create your views here.
from django.http import JsonResponse


def basket_summary(request):
    basket = Basket(request)
    context = {
        'basket':basket
    }
    return render(request, 'basket/basket_summary.html',context=context)

def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, quantity=product_qty)
        print("here")
        basket_quantity = basket.__len__()
        response = JsonResponse({'quantity':basket_quantity})
        return response

def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        basket.delete(product_id=product_id)
        new_count = basket.__len__()
        subtotal = basket.get_total_price()
        response = JsonResponse({'Success': True,
                                'new_count': new_count,
                                 'subtotal': subtotal,
                                 }
                                )
        return response

def basket_update(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        product_id = str(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        basket.update(product_id=product_id, product_quantity=product_qty)
        new_count = basket.__len__()
        new_sub_total = basket.get_total_price()
        response = JsonResponse({'Success':True,
                                 'new_count': new_count,
                                 'subtotal': new_sub_total,
                                 })
        return response
