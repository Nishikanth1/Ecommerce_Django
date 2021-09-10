from django.test import TestCase
#
# # Create your tests here.

from products.models import Category, Product, User

class TestCategoryModel(TestCase):
    def setUp(self):
        self.data1 = Category.objects.create(name='TestData1', slug='TestSlug1')

    def test_category_model_entry(self):
        data = self.data1
        self.assertTrue(isinstance(data,Category))

    def test_category_return_name(self):
        data = self.data1
        self.assertEqual(str(data), 'TestData1')


class TestProductsModel(TestCase):
    def setUp(self):
        Category.objects.create(name='TestData1', slug='TestSlug1')
        User.objects.create(username='admin')
        self.data1 = Product.objects.create(category_id=1, title='Title1', created_by_id=1,slug='slug1',
                                            price='20.00', image='image1')

    def test_product_model_entry(self):
        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'Title1')



