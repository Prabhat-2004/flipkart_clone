
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("add-to-cart/<int:product_id>/",
         views.add_to_cart, name="add_to_cart"),

    path("cart/", views.cart, name="cart"),
    path("cart/update/<int:product_id>/",
         views.update_cart, name="update_cart"),
    path("cart/remove/<int:product_id>/",
         views.remove_from_cart, name="remove_from_cart"),

    path("location/", views.location, name="location"),
    path("location/save/", views.save_location, name="save_location"),

    path("checkout/", views.checkout, name="checkout"),

    path("order-success/<int:order_id>/",
         views.order_success, name="order_success"),
]
