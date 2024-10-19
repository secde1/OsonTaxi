from rest_framework import serializers
from .models import Category, Product, Cart, Order


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'discount', 'status']  # Укажите только нужные поля


class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Cart
        fields = ['id', 'product', 'quantity']  # Указываем только нужные поля


class CartTotalSerializer(serializers.Serializer):
    total_price = serializers.FloatField()
    total_quantity = serializers.IntegerField()


class OrderSerializer(serializers.ModelSerializer):
    items = CartSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'items']  # Оставляем только нужные поля
