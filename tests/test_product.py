import random
import faker_commerce
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.core.management import call_command
from django.contrib.auth.models import User
from bangazon_api.helpers import STATE_NAMES
from bangazon_api.models import Category
from bangazon_api.models.product import Product


class ProductTests(APITestCase):
    def setUp(self):
        """
        Summary
        """
        call_command('seed_db', user_count=3)
        self.user1 = User.objects.filter(store__isnull=False).first()
        self.token = Token.objects.get(user=self.user1)

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.faker = Faker()
        self.faker.add_provider(faker_commerce.Provider)

    def test_create_product(self):
        """
        Ensure we can create a new product.
        """
        category = Category.objects.first()

        data = {
            "name": self.faker.ecommerce_name(),
            "price": random.randint(50, 1000),
            "description": self.faker.paragraph(),
            "quantity": random.randint(2, 20),
            "location": random.choice(STATE_NAMES),
            "imagePath": "",
            "categoryId": category.id
        }
        response = self.client.post('/api/products', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['id'])

    def test_update_product(self):
        """
        Ensure we can update a product.
        """
        product = Product.objects.first()
        data = {
            "name": product.name,
            "price": product.price,
            "description": self.faker.paragraph(),
            "quantity": product.quantity,
            "location": product.location,
            "imagePath": "",
            "categoryId": product.category.id
        }
        response = self.client.put(
            f'/api/products/{product.id}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        product_updated = Product.objects.get(pk=product.id)
        self.assertEqual(product_updated.description, data['description'])

    def test_get_all_products(self):
        """
        Ensure we can get a collection of products.
        """

        response = self.client.get('/api/products')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Product.objects.count())

    def test_delete_product(self):
        """_summary_
        """
        product = Product.objects.filter(store__seller=self.user1.id).first()

        response = self.client.delete(
            f'/api/products/{product.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_rate_product(self):
        """_summary_
        """
        product = Product.objects.first()
        rating = {
            "score": 3,
            "review": "Awesome product"
        }

        response = self.client.post(
            f'/api/products/{product.id}/rate_product', rating, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        response = self.client.get(f'/api/products/{product.id}')
        
        
        self.assertEqual(response.data["merchant_name"], data['merchant'])
        self.assertEqual(response.data["obscured_num"]
                         [-4:], data['acctNumber'][-4:])
        
        
