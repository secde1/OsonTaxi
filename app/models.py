from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Категория')
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        db_table = 'category'
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
        ordering = ("id",)

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS_CHOICES = [
        ('available', 'Доступен'),
        ('out_of_stock', 'Распродан'),
        ('discontinued', 'Снят с продажи'),
    ]

    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, verbose_name='Скидка в %')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    image = models.ImageField(upload_to='goods_images', blank=True, null=True, verbose_name='Изображение')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name='Статус')

    class Meta:
        db_table = 'product'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ("id",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:product", kwargs={"product_slug": self.slug})

    def display_id(self):
        return f"{self.id:05}"

    def sell_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)

        return self.price


# class CartQueryset(models.QuerySet):
#
#     def total_price(self):
#         return sum(cart.products_price() for cart in self)
#
#     def total_quantity(self):
#         if self:
#             return sum(cart.quantity for cart in self)
#         return 0


class Cart(models.Model):
    session_key = models.CharField(max_length=255, unique=True,
                                   verbose_name='Сессия')  # Сессия для пользователя без регистрации
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        db_table = 'cart'
        verbose_name = 'Карзина'
        verbose_name_plural = 'Карзина'
        ordering = ("id",)

    # def products_price(self):
    #     return round(self.product.sell_price() * self.quantity, 2)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('processed', 'Обработан'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]

    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    phone_number = models.CharField(max_length=20, verbose_name='Телефон')

    # Основной адрес доставки
    address = models.CharField(max_length=500, verbose_name='Адрес доставки')

    # Дополнительная информация для курьера (например, подъезд, ориентиры)
    delivery_instructions = models.TextField(verbose_name='Комментарий для курьера', blank=True, null=True)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая сумма')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    items = models.ManyToManyField(Cart, verbose_name='Товары')

    class Meta:
        db_table = 'order'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ("id",)

    def __str__(self):
        return f'Заказ #{self.id} - {self.first_name} {self.last_name}'

    def calculate_total(self):
        """Пересчитываем общую сумму заказа."""
        self.total_amount = sum(item.total_price() for item in self.items.all())
        self.save()
