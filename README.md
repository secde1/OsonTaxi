# 🛒 WebApp API Documentation

# Это документация для **WebApp**,

# REST API, которое предоставляет функционал для работы с категориями продуктов, корзиной и заказами.

# Категории

path('categories/', CategoryListAPIView.as_view(), name='category-list'), # Получение списка категорий ✅
path('categories/<int:id>/', CategoryDetailAPIView.as_view(), name='category-detail'), # Конкретная категория ✅

# Продукты

path('products/', ProductListAPIView.as_view(), name='product-list'), # Список всех продуктов ✅
path('products/<int:id>/', ProductDetailAPIView.as_view(), name='product-detail'), # Детали продукта ✅
path('products/search/', ProductSearchAPIView.as_view(), name='product-search'), # Поиск продуктов ✅

# Корзина

path('cart/', CartListAPIView.as_view(), name='cart-list'), # Получение всех товаров в корзине ✅
path('cart/add/', CartAddAPIView.as_view(), name='cart-add'), # Добавление товара в корзину ✅
path('cart/<int:id>/', CartUpdateAPIView.as_view(), name='cart-update'), # Обновление количества товара в корзине
path('cart/<int:id>/delete/', CartDeleteAPIView.as_view(), name='cart-delete'), # Удаление товара из корзины ✅

# Заказ

path('order/', OrderCreateAPIView.as_view(), name='order-create'), # Оформление заказа

# Склонируйте репозиторий: bash

    git clone https://github.com/secde1/webapp.git

# Перейдите в директорию проекта:

    cd webapp

# Создайте виртуальное окружение и активируйте его:

    python -m venv .venv
    source .venv/bin/activate

# Установите зависимости:

    pip install -r requirements.txt

# Примените миграции к базе данных:

    python manage.py migrate

# Запустите сервер разработки:

    python manage.py runserver