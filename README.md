# Это документация для **WebApp**,

# REST API, которое предоставляет функционал для работы с категориями продуктов, корзиной и заказами.

# Категории

Получение списка категорий ✅

    path('categories/', CategoryListAPIView.as_view(), name='category-list'),

Конкретная категория ✅

    path('categories/<int:id>/', CategoryDetailAPIView.as_view(), name='category-detail'),

# Продукты

Список всех продуктов ✅

    path('products/', ProductListAPIView.as_view(), name='product-list'),

Детали продукта ✅

    path('products/<int:id>/', ProductDetailAPIView.as_view(), name='product-detail'),

Поиск продуктов ✅

    path('products/search/', ProductSearchAPIView.as_view(), name='product-search'),

# Корзина

Получение всех товаров в корзине ✅

    path('cart/', CartListAPIView.as_view(), name='cart-list'),

Добавление товара в корзину ✅

    path('cart/add/', CartAddAPIView.as_view(), name='cart-add'),

Обновление количества товара в корзине ❌

    path('cart/<int:id>/', CartUpdateAPIView.as_view(), name='cart-update'),

Удаление товара из корзины ✅

    path('cart/<int:id>/delete/', CartDeleteAPIView.as_view(), name='cart-delete'),

# Заказ

Оформление заказа ❌

    path('order/', OrderCreateAPIView.as_view(), name='order-create'),


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