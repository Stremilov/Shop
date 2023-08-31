import csv
import json
from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from .models import Order


class OrderDetailViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='test_user', password='qwerty')
        permission_order = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(permission_order)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.order.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.order = Order.objects.create(
            delivery_adress= 'pupkina 9',
            promocode='123098',
            user=self.user,
        )

    def test_order_details(self):
        response = self.client.get(reverse('shopapp:order_details', kwargs={'pk': self.order.pk}))
        self.assertContains(response, self.order.delivery_adress)
        self.assertContains(response, self.order.promocode)
        received_data = response.context["order"].pk
        expected_data = self.order.pk
        self.assertEqual(received_data, expected_data)


class OrdersExportTestCase(TestCase):
    fixtures = [
        'orders-fixture.json'
    ]

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='test_user', password='qwerty')

    @classmethod
    def setUpTestData(cls):
        cls.orders = Order.objects.all()

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)


    def test_get_orders(self):
        response = self.client.get(reverse('shopapp:orders_list'))
        self.assertTemplateUsed(response, 'shopapp/order_list.html')
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            qs=self.orders,
            values=(response.context['orders']),
        )
