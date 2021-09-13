from django.contrib.auth.models import User
from django.test import  TestCase
from django.urls import reverse

from products.models import Category, Product

class TestBasketView(TestCase):
    def setUp(self):
        User.objects.create(username='admin')
        Category.objects.create(name="category_test", slug='testcategory')
        Product.objects.create(category_id=1,title='testProduct1',created_by_id=1,
                               slug='django-test1',
                               price='10.00', image='test_image')
        Product.objects.create(category_id=1,title='testProduct2',created_by_id=1,
                                   slug='django-test2',
                                   price='10.00', image='test_image')
        Product.objects.create(category_id=1, title='testProduct3', created_by_id=1,
                               slug='django-test3',
                               price='10.00', image='test_image')

        self.client.post(
            reverse('basket:basket_add'), {"product_id":1, "product_qty":1, "action": "post"}, xhr=True )
        self.client.post(
            reverse('basket:basket_add'), {"product_id":2, "product_qty":2, "action": "post"}, xhr=True )

    def test_basket_url(self):
        response = self.client.get(reverse('basket:basket_summary'))
        self.assertEqual(response.status_code, 200)

    def test_basket_add(self):
        response = self.client.post(reverse('basket:basket_add'), {"product_id":3, "product_qty":1, "action":"post"},
                                    xhr=True)
        self.assertEqual(response.json(), {"quantity": 4})
        response = self.client.post(reverse('basket:basket_add'), {"product_id":2, "product_qty":1, "action":"post"},
                                    xhr=True)
        self.assertEqual(response.json(), {"quantity": 3})

        # setup is per test so, data from above test is eraased and has data from setup only
    def test_basket_delete(self):
        response = self.client.post(reverse('basket:basket_delete'), {"product_id":2, "action":"post"},
                                    xhr=True)
        self.assertEqual(response.json(), {'Success': True, "new_count": 1, "subtotal": '10.00'})

    def test_basket_update(self):
        response = self.client.post(reverse('basket:basket_update'), {"product_id":2, "product_qty":1, "action":"post"},
                                    xhr=True)
        self.assertEqual(response.json(), {'Success': True, "new_count": 2, "subtotal": '20.00'})

