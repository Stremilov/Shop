from rest_framework import serializers

from shopapp.models import Models, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Models
        fields = 'pk', 'description', 'price', 'discount', 'created_time', 'archived', 'created_by',


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = 'delivery_adress', 'promocode', 'created_time', 'user', 'products',