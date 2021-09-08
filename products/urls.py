from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.all_products, name='all_products'),
    path('item/<int:id>/', views.product_detail, name='product_detail'),
    path('item/create/', views.product_create, name='product_create')
]