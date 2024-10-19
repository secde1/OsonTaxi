from django.db.models import Q
from rest_framework import status

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView, RetrieveUpdateDestroyAPIView

from .models import Category, Product, Order, Cart
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer, \
    CartTotalSerializer, CartSerializer


class CategoryListAPIView(GenericAPIView):
    serializer_class = CategorySerializer

    def get(self, request):
        category = Category.objects.all().order_by('-created_at')
        serializer_category = self.get_serializer(category, many=True)
        return Response(serializer_category.data)


class CategoryDetailAPIView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'


class ProductListAPIView(GenericAPIView):
    serializer_class = ProductSerializer

    def get(self, request):
        products = Product.objects.all()
        serializer_product = self.get_serializer(products, many=True)
        return Response(serializer_product.data)


class ProductGenericAPIView(GenericAPIView):
    serializer_class = ProductSerializer

    def get(self, request, category):
        product = Product.objects.filter(Q(category=category)).all()
        serializer_product = self.get_serializer(product, many=True)
        return Response(serializer_product.data)


class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


class SearchProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class CartListView(GenericAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get(self, request):
        cart = Cart.objects.all()
        serializer_cart = self.get_serializer(cart, many=True)
        return Response(serializer_cart.data)


# @csrf_protect
class CartAddView(APIView):
    def post(self, request, product_id):
        throttle_classes = [AnonRateThrottle]
        if not request.session.session_key:
            request.session.create()  # Создает новую сессию, если ее еще нет
        session_key = request.session.session_key  # Получаем session_key
        product = Product.objects.get(id=product_id)

        # Получаем или создаем объект Cart
        cart_item, created = Cart.objects.get_or_create(
            product=product,
            session_key=session_key,
            defaults={'quantity': 1}  # Или количество, переданное в запросе
        )

        if not created:
            cart_item.quantity += 1  # Увеличиваем количество, если товар уже есть в корзине
            cart_item.save()

        return Response({'message': 'Товар добавлен в корзину.'}, status=status.HTTP_201_CREATED)


class CartDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    lookup_url_kwarg = 'item_id'

    def perform_destroy(self, instance):
        super().perform_destroy(instance)


class IncrementCartAPIView(APIView):

    def post(self, request, pk):
        cart = get_object_or_404(Cart, pk=pk)
        cart.quantity += 1
        cart.save()
        return Response({"success": True, "message": "Количество товара успешно обновлено!"}, status=status.HTTP_200_OK)


class DecrementCartAPIView(APIView):

    def post(self, request, pk):
        cart = get_object_or_404(Cart, pk=pk)
        if cart.quantity > 1:
            cart.quantity -= 1
            cart.save()
            return Response({"success": True, "message": "Количество товара успешно обновлено!"})
        else:
            cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
