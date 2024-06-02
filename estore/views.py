from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Q


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


# Create your views here.
def index(request):
    products = Product.objects.all().order_by("-created_at")
    if request.user.is_authenticated:
        in_wishlist = set(WishList.objects.filter(user=request.user).values_list('product_id', flat=True))
        in_cart = set(CartItem.objects.filter(user=request.user).values_list('product_id', flat=True))
    else:
        in_wishlist = set()
        in_cart = set()

    context = {
        "title": "Главная страница",
        "products_f": products,
        "in_wishlist": in_wishlist,
        "in_cart": in_cart
    }

    return render(request, "html_files/index.html", context)


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            profile.save()
            messages.success(request, "Вы успешно прошли регистрацию!")
            return redirect("login")
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
            return redirect('sign-up')

    else:
        form = UserRegisterForm()

    context = {
        "title": "Регистрация пользователя",
        "form": form
    }

    return render(request, "html_files/sign-up.html", context)


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, "Вы успешно вошли в аккаунт!")
                return redirect("index")
            else:
                for field in form.errors:
                    messages.error(request, form.errors[field].as_text())
                return redirect('login')

        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
            return redirect('login')
    else:
        form = UserLoginForm()

    context = {
        "title": "Вход в аккаунт",
        "form": form
    }

    return render(request, "html_files/login.html", context)


def logout_view(request):
    logout(request)
    messages.info(request, "Вы вышли из аккаунта!")
    return redirect("index")


@login_required(login_url="login")
def profile_view(request, user_id):
    user = User.objects.get(id=user_id)
    profile = Profile.objects.get(user=user)

    context = {
        "user": user,
        "profile": profile,
        "title": "Профиль пользователя"
    }

    return render(request, "html_files/profile.html", context)


@login_required(login_url="login")
def edit_profile_view(request, profile_id):
    user = User.objects.get(id=profile_id)
    profile = Profile.objects.get(user=user)

    if request.method == "POST":

        user_form = UserForm(instance=user, data=request.POST)
        profile_form = ProfileForm(instance=profile,
                                   data=request.POST,
                                   files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Изменения внесены успешно!")
            return redirect("profile", profile_id)
        else:
            for field in user_form.errors:
                messages.error(request, user_form.errors[field].as_text())
            for field in profile_form.errors:
                messages.error(request, profile_form.errors[field].as_text())
            return redirect("edit-profile", profile_id)

    else:

        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "title": "Изменение профиля"
    }

    return render(request, "html_files/edit-profile.html", context)


def pr_category_list_view(request, category_id):
    category = Category.objects.get(id=category_id)
    pr_categories = ProductCategory.objects.filter(category=category)

    context = {
        "pr_categories": pr_categories,
        "category": category
    }

    return render(request, "html_files/product-sub-category-list.html", context)


def pr_category_product_list_view(request, pr_category_id):
    pr_category = ProductCategory.objects.get(id=pr_category_id)
    products = Product.objects.filter(category=pr_category)
    if request.user.is_authenticated:
        in_wishlist = set(WishList.objects.filter(user=request.user).values_list('product_id', flat=True))
        in_cart = set(CartItem.objects.filter(user=request.user).values_list('product_id', flat=True))
    else:
        in_wishlist = set()
        in_cart = set()

    context = {
        "pr_category": pr_category,
        "products": products,
        "in_wishlist": in_wishlist,
        "in_cart": in_cart
    }

    return render(request, "html_files/product-list.html", context)


def product_detail_view(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        reviews = ProductReview.objects.filter(product=product).order_by('-created_at')
        characteristics = Characteristic.objects.filter(product=product)

        if request.user.is_authenticated:
            in_cart = CartItem.objects.filter(user=request.user, product=product).exists()
            in_wishlist = WishList.objects.filter(product=product, user=request.user).exists()
        else:
            in_cart = None
            in_wishlist = None
    except Exception as e:
        raise e

    context = {
        "title": "Детали товара",
        "product": product,
        "reviews": reviews,
        "characteristics": characteristics,
        "in_cart": in_cart,
        "in_wishlist": in_wishlist
    }

    return render(request, "html_files/product-detail.html", context)


@login_required(login_url="login")
# comment
def add_review_view(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.method == "POST":
        form = ProductReviewForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            messages.success(request, "Отзыв успешно добавлен!")
            return redirect("product-detail", product_id)
        else:
            messages.error(request, "Ошибка. Повторите попытку!")
    else:

        form = ProductReviewForm()

    context = {
        "title": "Оставление отзыва",
        "form": form,
        "product": product
    }

    return render(request, "html_files/add_review.html", context)


def search(request):
    query = request.GET.get('q')

    products = Product.objects.filter(Q(title__icontains=query) | Q(desc__icontains=query) |
                                      Q(category__title__icontains=query) |
                                      Q(category__category__title__icontains=query) |
                                      Q(tags__title__icontains=query) |
                                      Q(short_desc__icontains=query) |
                                      Q(product_characteristics__title__icontains=query)).order_by("-created_at")

    context = {
        "query": query,
        "products": products,
    }

    return render(request, "html_files/search.html", context)


@login_required(login_url="login")
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

    if request.user.is_authenticated:
        try:
            cart_item = CartItem.objects.get(product=product, user=request.user)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
                user=request.user
            )
        cart_item.save()
    else:
        return messages.warning(request, "Что-то пошло не так. Повторите попытку!")

    return redirect('cart')


@login_required(login_url="login")
def decrement_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        messages.error(request, "Ошибка. Что-то пошло не так!")

    return redirect('cart')


@login_required(login_url="login")
def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart_item = CartItem.objects.filter(product=product, user=request.user)

    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.filter(product=product, cart=cart)

    cart_item.delete()
    messages.info(request, "Товар удален из корзины!")

    return redirect('cart')


@login_required(login_url="login")
def cart_view(request, total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, status=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, status=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    except ObjectNotExist:
        pass

    context = {
        "title": "Корзина",
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items
    }

    return render(request, "html_files/cart.html", context)


@login_required(login_url="login")
def add_to_wishlist(request, product_id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)

        wishlist_item, created = WishList.objects.get_or_create(product=product, user=request.user)

        if created:
            messages.success(request, "Товар успешно добавлен в избранное!")
    else:
        pass

    return redirect("wishlist")


@login_required(login_url="login")
def remove_from_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)

    try:
        wishlist_item = WishList.objects.get(product=product, user=request.user)
        wishlist_item.delete()
        messages.info(request, "Товар удален из избранного!")
    except WishList.DoesNotExist:
        messages.info(request, "Нет такого товара в избранном!")

    return redirect("wishlist")


@login_required(login_url="login")
def wishlist_view(request):
    if request.user.is_authenticated:
        wishlist_items = WishList.objects.filter(user=request.user)
    else:
        wishlist_items = []
    context = {
        "title": "Избранное",
        "wishlist_items": wishlist_items
    }

    return render(request, "html_files/wishlist.html", context)


@login_required(login_url="login")
def checkout_view(request, total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, status=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, status=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect("index")

    if request.method == "POST":
        form = OrderForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = current_user
            total_price = total
            order.total_price = Order.objects.get(total_price=total_price)
            order.save()
            messages.success(request, "Заказ принят на обработку!")
            return redirect("index")
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
            return redirect('checkout')
    else:
        form = OrderForm()

    context = {
        "title": "Заказ",
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "form": form
    }

    return render(request, "html_files/checkout.html", context)


def about_us(request):

    context = {
        "title": "О нас"
    }

    return render(request, "html_files/about_us.html", context)







