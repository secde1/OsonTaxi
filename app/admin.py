from django.contrib import admin
from .models import Category, Product, Cart, Order


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'discount', 'status')
    search_fields = ('name', 'category__name')
    list_filter = ('category', 'status')


@admin.register(Cart)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'session_key')
    search_fields = ('session_key', 'product__name')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'total_amount', 'status', 'created_at')
    search_fields = ('first_name', 'last_name', 'phone_number')
    list_filter = ('status',)
