from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.core.management import call_command
from django.contrib.auth.models import User

from bangazon_api.models import Order, Product, PaymentType
from bangazon_api.serializers.order_serializer import OrderSerializer


class OrderTests(APITestCase):
    def setUp(self):
        """
        Seed the database
        """
        call_command('seed_db', user_count=3)
        self.user1 = User.objects.filter(store=None).first()
        self.token = Token.objects.get(user=self.user1)

        self.user2 = User.objects.filter(store=None).last()
        product = Product.objects.get(pk=1)

        self.order1 = Order.objects.create(
            user=self.user1
        )

        self.order1.products.add(product)

        self.order2 = Order.objects.create(
            user=self.user2
        )

        self.order2.products.add(product)

        # Create a new instance of PaymentType
        self.payment_type = PaymentType()
        self.payment_type.merchant_name = "Discover"
        self.payment_type.acct_number = 1234123412341234
        self.payment_type.customer = self.user1

        # Save the PaymentType to the testing database
        self.payment_type.save()

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_list_orders(self):
        """The orders list should return a list of orders for the logged in user"""
        response = self.client.get('/api/orders')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        

    def test_delete_order(self):
        """_summary_
        """
        response = self.client.delete(f'/api/orders/{self.order1.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_complete_order(self):
        """The orders list should return a list of orders for the logged in user"""

        url = f"/api/orders/{self.order1.id}/complete"

        body = {"paymentTypeId": self.payment_type.id}

        # Initiate PUT request and capture the response
        response = self.client.put(url, body, format="json")

        # Assert that the response status code is 204 (NO CONTENT)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # There is no retrieve for orders, so use the get orm on the Order model
        order = Order.objects.get(pk=self.order1.id)
        response = OrderSerializer(order)

        self.assertIsNotNone(response.data["completed_on"])
        self.assertEqual(response.data["payment_type"]["id"], self.payment_type.id)
