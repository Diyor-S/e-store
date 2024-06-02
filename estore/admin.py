from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'created_at', 'image', 'address']
    list_filter = ['created_at']
    search_fields = ['phone_number']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category']
    list_filter = ['category']
    search_fields = ['category']


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'category']
    list_filter = ['created_at']
    search_fields = ['category']


class ProductImageAdmin(admin.TabularInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'status', 'image', 'tags', 'price', 'rating',
                    'category', 'get_discount_percentage']
    list_filter = ['created_at']
    search_fields = ['title']
    inlines = [ProductImageAdmin]


@admin.register(ProductCharacteristic)
class ProductCharacteristicAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'product']
    list_filter = ['product']
    search_fields = ['title']


@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'product']
    list_filter = ['product']
    search_fields = ['title']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'phone_number', 'status',
                    'ordered_at']
    list_filter = ['status']
    search_fields = ['status']


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product',
                    'price', 'quantity', 'image', 'total_price']
    list_filter = ['order']
    search_fields = ['order']


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'created_at', 'rating', 'review']
    list_filter = ['created_at']
    search_fields = ['product']


@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ['product', 'added_at']
    list_filter = ['added_at']
    search_fields = ['product']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart_id', 'created_at']
    list_filter = ['created_at']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'quantity', 'status']
    list_filter = ['product']






