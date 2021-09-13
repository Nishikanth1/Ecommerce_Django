from unittest import skip
from importlib import  import_module

from django.http import  HttpRequest
from django.conf import  settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import  Client,TestCase, RequestFactory

from products.models import Category, Product, User
from products.views import all_products


@skip("skipping example")
class TestSkip(TestCase):
    def test_skip_example(self):
        pass


class TestViewResponses(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        User.objects.create(username="admin")
        Category.objects.create(name="category_test", slug='testcategory')
        Product.objects.create(category_id=1,title='testProduct',created_by_id=1,
                               slug='django-test',
                               price='21.99', image='test_image')


    def test_url_allowed_host(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code ,200)

    def test_product_detail_url(self):
        response = self.client.get(reverse('products:product_detail',args=['1']))
        self.assertEqual(response.status_code, 200)

    def test_category_detail_url(self):
        response = self.client.get(reverse('products:category_list',args=['testcategory']))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        response = all_products(request)
        html = response.content.decode('utf-8')
        #print(html)
        self.assertIn('WebShopy', html)

    def test_view_function(self):
        request = self.factory.get('/item/1')
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()

        response = all_products(request)
        html = response.content.decode('utf-8')
        print(html)
        #self.assertIn('WebShopy', html)


def test_homepage_url(self):
    """
    test homepage
    """
    response = self.Client.get("/")