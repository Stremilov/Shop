from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from myapiapp.cerializers import ProductSerializer, OrderSerializer
from shopapp.models import Models, Order


class ProductsListView(APIView):
    def get(self, request: Request) -> Response:
        products = Models.objects.all()
        serialized = ProductSerializer(products, many=True)
        return Response({'Products': serialized.data})


class OrdersListView(APIView):
    def get(self, request: Request) -> Response:
        products = Order.objects.all()
        serialized = OrderSerializer(products, many=True)
        return Response({'Orders': serialized.data})
