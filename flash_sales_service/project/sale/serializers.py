from rest_framework import serializers

from .models import Order, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "description", "price", "stock")
        read_only_fields = fields


class ProductStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "stock")
        read_only_fields = fields


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("product", "quantity")


class OrderResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "product", "quantity", "created_at")
        read_only_fields = fields
