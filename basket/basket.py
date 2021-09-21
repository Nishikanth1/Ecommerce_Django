from django.shortcuts import get_object_or_404

from products.models import Product
from decimal import Decimal

class Basket(object):
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        print("init")
        #print(str(request.session.__str__))
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}

        self.basket = basket

    def __iter__(self):
        """
        uses IDs of products in Session and queries the database
        to return products
        """
        product_ids = self.basket.keys()
        #products = Product.products.filter(id__in=product_ids)
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()
        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield(item)

    def add(self, product, quantity):
        product_id = str(product.id)
        print("product id is {0}".format(product_id))
        if product_id in self.basket:
            self.basket[product_id]['quantity'] = int(quantity)
        else:
            self.basket[product_id] = {'price':str(product.price),
                                       'quantity': int(quantity),
                                       }
            print("here")
            print(self.basket[product_id])
        self.save()

    def __len__(self):
        """
        Get the basket data and quantity of items

        """
        total_qty = sum(item['quantity'] for item in self.basket.values())
        print("total qty is {0}".format(total_qty))
        print("basket is {0}".format(self.basket))
        return sum(item['quantity'] for item in self.basket.values())

    def get_total_price(self):
        return sum(Decimal(item['price'])*item['quantity'] for item in self.basket.values())

    def delete(self, product_id):
        product_id = str(product_id)
        print("product id while deleting is {0}".format(type(product_id)))
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def update(self, product_id, product_quantity):
        product_id = str(product_id)
        product_quantity = product_quantity
        if product_id in self.basket:
            self.basket[product_id]['quantity'] = product_quantity
        print(" id is {0} qty is {1}".format(product_id, product_quantity))
        self.save()

    def save(self):
        self.session.modified = True