from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.core.management import call_command
from django.contrib.auth.models import User

from bangazon_api.models.payment_type import PaymentType


class PaymentTests(APITestCase):
    def setUp(self):
        """
        Seed the database
        """
        call_command('seed_db', user_count=3)
        self.user1 = User.objects.filter(store=None).first()
        self.token = Token.objects.get(user=self.user1)

        # Create a new instance of PaymentType
        self.payment_type = PaymentType()
        self.payment_type.merchant_name = "Discover"
        self.payment_type.acct_number = 1234123412341234
        self.payment_type.customer = self.user1

        # Save the PaymentType to the testing database
        self.payment_type.save()

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.faker = Faker()

    def test_create_payment_type(self):
        """
        Ensure we can add a payment type for a customer.
        """
        # Add product to order
        data = {
            "merchant": self.faker.credit_card_provider(),
            "acctNumber": self.faker.credit_card_number()
        }

        response = self.client.post('/api/payment-types', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['id'])
        self.assertEqual(response.data["merchant_name"], data['merchant'])
        self.assertEqual(response.data["obscured_num"]
                         [-4:], data['acctNumber'][-4:])

    def test_delete_payment(self):
        """_summary_
        """
        response = self.client.delete(
            f'/api/payment-types/{self.payment_type.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
