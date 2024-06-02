from .models import *
from .views import _cart_id


def default(request):

    products = Product.objects.all()
    categories = Category.objects.all()
    reviews = ProductReview.objects.all()
    product_categories = ProductCategory.objects.all()
    product_characteristics = ProductCharacteristic.objects.all()
    characteristic = Characteristic.objects.all()
    profiles = Profile.objects.all()

    return {
        "categories": categories,
        "reviews": reviews,
        "products": products,
        "pr_categories": product_categories,
        "pr_characteristics": product_characteristics,
        "characteristic": characteristic,
        "profiles": profiles


    }


def cart_default(request):
    cart_count = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.all().filter(user=request.user)
        else:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            cart_items = CartItem.objects.all().filter(cart=cart[:1])

        for cart_item in cart_items:
            cart_count += cart_item.quantity
    except Cart.DoesNOtExist:
        cart_count = 0
    return dict(cart_count=cart_count)


def cart_total(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, status=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    except:
        pass
    return {
        "total": total,
        "cart_items": cart_items
    }


def wishlist_default(request):

    if request.user.is_authenticated:

        wishlist_items = WishList.objects.filter(user=request.user)
    else:
        wishlist_items = 0

    return {
        "wishlist_items": wishlist_items
    }


