from django.db import models
from django.utils import timezone

from .utils import validate_phone_number

from django.contrib.auth.models import User


# Create your models here.


# Categories such as Electronics, Furniture, Books, for Kitchen, etc.
class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name="Категория", unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:  # for admin panel
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class Profile(models.Model):  # Profile of the user
    phone_number = models.CharField(max_length=20, validators=[validate_phone_number], verbose_name="Номер телефона")
    address = models.CharField(max_length=120, verbose_name="Адрес")
    image = models.FileField(upload_to="profiles/", null=True, blank=True, verbose_name="Фото пользователя")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    about = models.TextField(verbose_name="О себе", null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="user_profiles")

    class Meta:  # for admin panel
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):  # to return the title itself not an 'object'
        return self.user.username


class Tag(models.Model):  # Tags for products based on category
    title = models.CharField(max_length=200, verbose_name="Тэги")
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 verbose_name="Категория",
                                 related_name="tags")

    class Meta:  # for admin panel
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self):
        return self.title


class ProductCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name="Категория продукта")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория",
                                 related_name="category")
    image = models.FileField(upload_to='sub-categories/', null=True, blank=True,
                             verbose_name="фото подкатегории продукта")

    class Meta:
        verbose_name = "Категория продукта"
        verbose_name_plural = "Категории продуктов"

    def __str__(self):
        return self.title


ProductRating = (
    ("★☆☆☆☆", "★☆☆☆☆"),
    ("★★☆☆☆", "★★☆☆☆"),
    ("★★★☆☆", "★★★☆☆"),
    ("★★★★☆", "★★★★☆"),
    ("★★★★★", "★★★★★")
)


class Product(models.Model):  # products linked to category : they have title, image, tags linked to class 'Tag'
    # short_desc --> little info, desc --> details, discount --> which product will have, price and old_price --> to
    # attract customers
    # created_at --> the date when product was added, updated_at --> when was the last change in product
    # status --> whether product is still available or not
    # category --> each product belongs to a particular category

    title = models.CharField(max_length=120, verbose_name="Название продукта")
    image = models.FileField(upload_to="products/", null=True, blank=True,
                             verbose_name="Фото продукта", default="product.jpg")
    tags = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="Тэги продукта",
                             related_name="product_tags")
    short_desc = models.TextField(null=True, blank=True, verbose_name="Короткое описание продукта")
    desc = models.TextField(null=True, blank=True, verbose_name="Описание продукта")
    price = models.DecimalField(max_digits=999999999999, decimal_places=2, default="1.99", verbose_name="Цена")
    old_price = models.DecimalField(max_digits=999999999999, decimal_places=2, default="2.99",
                                    verbose_name="Старая цена")
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата обновления")
    status = models.BooleanField(default=True, verbose_name="Активно")
    rating = models.CharField(max_length=30, verbose_name="Рейтинг", null=True, blank=True, default=None,
                              choices=ProductRating)

    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE,
                                 verbose_name="Категория продукта",
                                 related_name="product_category")

    class Meta:  # admin panel
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):  # return ID and Title of the product
        return f" ID: {self.id} | Название продукта: {self.title}"

    @property
    def get_discount_percentage(self):  # to get the difference in percentage between new_price and old_price
        new_price = (((self.old_price - self.price) / self.old_price) * 100)
        return int(new_price)

    @property
    def get_main_category(self):
        return self.category.category


class ProductImage(models.Model):  # each product can have multiple 'images' so we get them into 'products' directory
    # in media ; product --> image belongs to particular product ; created_at --> when was the image added
    images = models.FileField(upload_to="products/", default="product.jpg", verbose_name="Фото продукта")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, verbose_name="Продукт")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:  # admin panel
        verbose_name = "Фотография продукта"
        verbose_name_plural = "Фотографии продукта"

    def __str__(self):
        return self.product.title


class ProductCharacteristic(models.Model):  # characteristic of the product --> desc ; title ; linked to 'product'
    title = models.CharField(max_length=120, verbose_name="Название характеристики продукта")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт",
                                related_name="product_characteristics")

    class Meta:  # admin panel
        verbose_name = "Название характеристики продукта"
        verbose_name_plural = "Название характеристики продуктов"

    def __str__(self):
        return self.title


class Characteristic(models.Model):
    characteristic = models.TextField(verbose_name="Характеристика продукта")

    title = models.ForeignKey(ProductCharacteristic, on_delete=models.CASCADE,
                              verbose_name="Название характеристики продукта")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт",
                                related_name="characteristics")

    class Meta:
        verbose_name = "Характеристики продукта"
        verbose_name_plural = "Характеристики продуктов"

    def __str__(self):
        return self.title.title


class Order(models.Model):  # Order --> full_name --- info about the person who made this order; his phone_number
    # status --> whether the order is 'new', 'accepted', 'in_progress' of delivering, 'cancelled' and
    # 'finished'- delivered
    # total_price -- the amount of money for order ; ordered_at -- the date when was the product ordered

    # user -- which user ordered it

    class OrderStatus(models.TextChoices):
        NEW = "NEW", "НОВЫЙ"
        ACCEPTED = "ACCEPTED", "ПРИНЯТ"
        IN_PROGRESS = "IN PROGRESS", "В ПРОЦЕССЕ"
        CANCELLED = "CANCELLED", "ОТМЕНЕН"
        FINISHED = "FINISHED", "ЗАВЕРШЁН"

    full_name = models.CharField(max_length=120, verbose_name="Полное имя")
    phone_number = models.CharField(max_length=120, validators=[validate_phone_number],
                                    verbose_name="Номер телефона")
    address = models.CharField(max_length=120, verbose_name="Адрес", default=None)
    email = models.EmailField(verbose_name="Электронная почта", default=None)
    order_note = models.TextField(verbose_name="Комментарий к заказу", null=True, blank=True)
    status = models.CharField(max_length=120, verbose_name="Статус заказа",
                              choices=OrderStatus.choices,
                              default=OrderStatus.NEW)
    total_price = models.FloatField(default=0, verbose_name="Итого")
    ordered_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Дата заказа")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Кто заказывает")

    class Meta:  # admin panel
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):  # return full_name of the person not 'object'
        return self.full_name


class OrderProduct(models.Model):  # OrderProduct --> order --- linked to Order to understand which order is it;
    # product --- product belongs to which order ; image --- upload the image of the product ;
    # price -- how much product costs ; quantity --- how many products are being ordered;
    # total_price --- the function which evaluates the total cost of the product by using arguments price and quantity

    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ продукта")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт",
                                related_name="product_orders")
    image = models.ForeignKey(ProductImage, on_delete=models.CASCADE, null=True, verbose_name="Фото продукта")
    price = models.DecimalField(max_digits=999999999999, decimal_places=2, default="1.99")
    quantity = models.IntegerField(verbose_name="Количество заказанных продуктов", default=0)
    total_price = models.DecimalField(max_digits=999999999999, decimal_places=2, default="1.99")

    class Meta:  # admin panel
        verbose_name = "Заказ Продукта"
        verbose_name_plural = "Заказ продуктов"
        unique_together = ['order', 'product']

    def __str__(self):  # return ID and Title of the product
        return f"ID: {self.id} | Количество: {self.product.title}"

    @property
    def total_price(self):  # the function evaluates total cost
        return self.price * self.quantity


# ProductRating --- > the rating of the product ; how good is it


class ProductReview(models.Model):  # Review of the product ---> product -- review of which product;
    # review -- desc, info and explanation, rating --> choices=ProductRating --- how good the product is
    # created_at --- date  when the review was added
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="Пользователь")

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт", related_name="reviews")
    review = models.TextField()
    rating = models.CharField(choices=ProductRating, default=None, max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:  # admin panel
        verbose_name = "Обзор продукта"
        verbose_name_plural = "Обзоры продукта"

    def __str__(self):  # title of the product
        return self.product.title


class WishList(models.Model):  # WishList --> product --- which product to add into wishlist; added_at --- when was
    # the product added to wishlist
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлено в")

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", default=None)

    class Meta:  # admin panel
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"

    def __str__(self):  # to get Title of the product and its ID
        return f"ID: {self.id} | Product: {self.product.title}"


class Cart(models.Model):
    cart_id = models.CharField(max_length=100, verbose_name="Номер корзины", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="продукт")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name="корзина")
    quantity = models.PositiveIntegerField(default=1)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Товар корзины"
        verbose_name_plural = "Товары корзины"

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.title