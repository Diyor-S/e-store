from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("sign-up/", register_view, name="sign-up"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/<int:user_id>/", profile_view, name="profile"),
    path("edit-profile/<int:profile_id>/", edit_profile_view, name="edit-profile"),

    path('categories/<int:category_id>/', pr_category_list_view, name="sub-category-list"),
    path('pr_category-product-list/<int:pr_category_id>/', pr_category_product_list_view,
         name="pr_category-product-list"),

    path('product-detail/<int:product_id>/', product_detail_view, name="product-detail"),
    path('add-review/<int:product_id>/', add_review_view, name="add-review"),
    path('search/', search, name="search"),
    path('add_to_cart/<int:product_id>/', add_to_cart, name="add-to-cart"),
    path('decrement_from_cart/<int:product_id>/', decrement_from_cart, name="decrement-from-cart"),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name="remove-from-cart"),
    path('cart/', cart_view, name="cart"),
    path('wishlist/', wishlist_view, name="wishlist"),
    path('add-to-wishlist/<int:product_id>/', add_to_wishlist, name="add-to-wishlist"),
    path('remove-from-wishlist/<int:product_id>/', remove_from_wishlist, name="remove-from-wishlist"),

    path('checkout/', checkout_view, name="checkout"),

    path('about-us', about_us, name="about-us")
]