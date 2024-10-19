from django.urls import path

from .views import CategoryListAPIView, CategoryDetailAPIView, ProductGenericAPIView, ProductListAPIView, \
    ProductDetailAPIView, SearchProductListAPIView, CartListView, CartDetailView, CartAddView, IncrementCartAPIView, \
    DecrementCartAPIView

urlpatterns = [
    # Категории
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),  # Получение списка категорий
    path('categories/<int:id>/', CategoryDetailAPIView.as_view(), name='category-detail'),  # Конкретная категория
    # Продукты
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:id>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('products/category/<int:category>', ProductGenericAPIView.as_view(), name='category-products'),
    path('products/search/', SearchProductListAPIView.as_view(), name='product-search'),
    # Корзина
    path('cart/', CartListView.as_view(), name='cart-list'),  # Список всех товаров в корзине
    path('cart/add/<int:product_id>/', CartAddView.as_view(), name='cart-add-product'),  # Добавление товара в корзину
    path('cart/<int:item_id>/', CartDetailView.as_view(), name='cart-detail'),  # Детали товара в корзине

    # path('cart/total', CartTotalView.as_view(), name='cart-total'),

    # Управление количеством товаров в корзине
    path('increment-product/<int:pk>', IncrementCartAPIView.as_view(), name='increment_product'),
    path('decrement-product/<int:pk>', DecrementCartAPIView.as_view(), name='decrement_product'),

]
