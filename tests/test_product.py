import random

import faker_commerce
from bangazon_api.helpers import STATE_NAMES
from bangazon_api.models import Category, Product
from django.contrib.auth.models import User
from django.core.management import call_command
from faker import Faker
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from bangazon_api.models.order_product import OrderProduct


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
        new_rating = {
            "score": 3,
            "review": "Awesome product"
        }

        response = self.client.post(
            f'/api/products/{product.id}/rate-product', new_rating, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(f'/api/products/{product.id}')

        total_rating = 0

        for rating in product.ratings.all():
            total_rating += rating.score

        new_average = total_rating / product.ratings.count()

        self.assertGreater(response.data["average_rating"], 0)
        self.assertEqual(response.data["average_rating"], new_average)

    def test_add_product_to_order(self):
        """_summary_
        """
        product = Product.objects.first()

        response = self.client.post(
            f'/api/products/{product.id}/add_to_order', format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get('/api/orders/current')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        existing_order_product = OrderProduct.objects.get(
            order=response.data["id"], product=product)

        self.assertIsNotNone(existing_order_product)
