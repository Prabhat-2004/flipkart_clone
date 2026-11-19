
from decimal import Decimal

from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from .models import Category, Product, Order, OrderItem


def get_cart_data(request):
    cart = request.session.get("cart", {})
    items = []
    total = Decimal("0.00")
    clean_cart = {}

    for product_id, quantity in cart.items():
        try:
            quantity = int(quantity)

            if quantity <= 0:
                continue

            product = Product.objects.get(
                id=product_id,
                is_available=True
            )

            quantity = min(quantity, product.stock)

            if quantity <= 0:
                continue

            price = (
                product.discount_price
                if product.discount_price is not None
                else product.price
            )

            line_total = price * quantity

            items.append({
                "product": product,
                "quantity": quantity,
                "price": price,
                "line_total": line_total,
            })

            clean_cart[str(product.id)] = quantity
            total += line_total

        except (Product.DoesNotExist, ValueError, TypeError):
            continue

    request.session["cart"] = clean_cart

    return items, total


def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)

    search = request.GET.get("search", "").strip()
    category_id = request.GET.get("category", "").strip()

    if search:
        products = products.filter(name__icontains=search)

    if category_id:
        try:
            products = products.filter(category_id=int(category_id))
        except ValueError:
            pass

    items, total = get_cart_data(request)
    cart_count = sum(item["quantity"] for item in items)

    context = {
        "categories": categories,
        "products": products,
        "cart_count": cart_count,
        "search": search,
        "selected_category": category_id,
        "delivery_location": request.session.get(
            "delivery_location", {}
        ),
    }

    return render(
        request,
        "delivery_app/index.html",
        context
    )


def add_to_cart(request, product_id):
    if request.method == "POST":

        product = get_object_or_404(
            Product,
            id=product_id,
            is_available=True
        )

        cart = request.session.get("cart", {})
        product_id = str(product.id)

        current_quantity = int(cart.get(product_id, 0))

        if current_quantity < product.stock:

            cart[product_id] = current_quantity + 1
            request.session["cart"] = cart

            messages.success(
                request,
                f"{product.name} added to cart!"
            )

        else:
            messages.warning(
                request,
                "Available stock limit reached."
            )

    return redirect("home")


def cart(request):

    items, total = get_cart_data(request)

    return render(
        request,
        "delivery_app/cart.html",
        {
            "items": items,
            "total": total,
            "cart_count": sum(
                item["quantity"] for item in items
            ),
        }
    )


def update_cart(request, product_id):

    if request.method == "POST":

        cart_data = request.session.get("cart", {})

        product = get_object_or_404(
            Product,
            id=product_id
        )

        try:
            quantity = int(
                request.POST.get("quantity", 1)
            )
        except (ValueError, TypeError):
            quantity = 1

        if quantity <= 0:
            cart_data.pop(str(product_id), None)

        elif quantity > product.stock:

            messages.warning(
                request,
                f"Only {product.stock} units of {product.name} are available."
            )

            if product.stock:
                cart_data[str(product_id)] = product.stock
            else:
                cart_data.pop(str(product_id), None)

        else:
            cart_data[str(product_id)] = quantity

        request.session["cart"] = cart_data

    return redirect("cart")


def remove_from_cart(request, product_id):

    if request.method == "POST":

        cart_data = request.session.get("cart", {})

        cart_data.pop(str(product_id), None)

        request.session["cart"] = cart_data

        messages.success(
            request,
            "Product removed from cart."
        )

    return redirect("cart")


def location(request):

    saved_location = request.session.get(
        "delivery_location", {}
    )

    return render(
        request,
        "delivery_app/location.html",
        {
            "saved_location": saved_location,
        }
    )


def save_location(request):

    if request.method == "POST":

        house_address = request.POST.get(
            "house_address", ""
        ).strip()

        landmark = request.POST.get(
            "landmark", ""
        ).strip()

        city = request.POST.get(
            "city", ""
        ).strip()

        pincode = request.POST.get(
            "pincode", ""
        ).strip()

        latitude = request.POST.get(
            "latitude", ""
        ).strip()

        longitude = request.POST.get(
            "longitude", ""
        ).strip()

        if not house_address or not city or not pincode:

            messages.error(
                request,
                "Please enter your address, city and PIN code."
            )

            return redirect("location")

        full_address = house_address

        if landmark:
            full_address += ", " + landmark

        full_address += f", {city} - {pincode}"

        request.session["delivery_location"] = {
            "address": full_address,
            "house_address": house_address,
            "landmark": landmark,
            "city": city,
            "pincode": pincode,
            "latitude": latitude,
            "longitude": longitude,
        }

        messages.success(
            request,
            "Delivery location saved!"
        )

        if request.session.get("cart"):
            return redirect("cart")

        return redirect("home")

    return redirect("location")


def checkout(request):

    items, total = get_cart_data(request)

    if not items:

        messages.warning(
            request,
            "Your cart is empty."
        )

        return redirect("home")

    saved_location = request.session.get(
        "delivery_location"
    )

    if not saved_location:

        messages.info(
            request,
            "Please set your delivery location first."
        )

        return redirect("location")

    if request.method == "POST":

        customer_name = request.POST.get(
            "customer_name", ""
        ).strip()

        phone = request.POST.get(
            "phone", ""
        ).strip()

        payment_method = request.POST.get(
            "payment_method", "cod"
        )

        if not customer_name or not phone:

            messages.error(
                request,
                "Enter your name and phone number."
            )

            return redirect("checkout")

        if payment_method not in ("cod", "upi", "card"):

            messages.error(
                request,
                "Please select a valid payment method."
            )

            return redirect("checkout")

        try:

            with transaction.atomic():

                fresh_items = []
                final_total = Decimal("0.00")

                for item in items:

                    product = Product.objects.select_for_update().get(
                        id=item["product"].id
                    )

                    quantity = item["quantity"]

                    if (
                        not product.is_available
                        or product.stock < quantity
                    ):

                        raise ValueError(
                            f"Insufficient stock for {product.name}. "
                            "Please update your cart."
                        )

                    price = (
                        product.discount_price
                        if product.discount_price is not None
                        else product.price
                    )

                    final_total += price * quantity

                    fresh_items.append(
                        (product, quantity, price)
                    )

                order = Order.objects.create(
                    customer_name=customer_name,
                    phone=phone,
                    delivery_address=saved_location["address"],
                    city=saved_location["city"],
                    pincode=saved_location["pincode"],
                    latitude=saved_location.get("latitude", ""),
                    longitude=saved_location.get("longitude", ""),
                    payment_method=payment_method,
                    payment_status="Pending",
                    total_amount=final_total,
                )

                for product, quantity, price in fresh_items:

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        product_name=product.name,
                        price=price,
                        quantity=quantity,
                    )

                    product.stock -= quantity

                    product.save(
                        update_fields=["stock"]
                    )

            # Save the order ID in the current session
            request.session["last_order_id"] = order.id

            # Clear the shopping cart
            request.session["cart"] = {}

            return redirect(
                "order_success",
                order_id=order.id
            )

        except (ValueError, Product.DoesNotExist) as error:

            messages.error(request, str(error))

            return redirect("cart")

    return render(
        request,
        "delivery_app/checkout.html",
        {
            "items": items,
            "total": total,
            "saved_location": saved_location,
        }
    )


def order_success(request, order_id):

    # Verify that this order belongs to the current session
    if request.session.get("last_order_id") != order_id:

        return redirect("home")

    order = get_object_or_404(
        Order,
        id=order_id
    )

    return render(
        request,
        "delivery_app/order_success.html",
        {
            "order": order,
        }
    )
