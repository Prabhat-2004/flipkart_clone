
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Category, Product


def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)

    search = request.GET.get('search', '')
    category_id = request.GET.get('category', '')

    if search:
        products = products.filter(name__icontains=search)

    if category_id:
        products = products.filter(category_id=category_id)

    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())

    context = {
        'categories': categories,
        'products': products,
        'cart_count': cart_count,
        'search': search,
        'selected_category': category_id,
    }

    return render(request, 'delivery_app/index.html', context)


def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(
            Product,
            id=product_id,
            is_available=True
        )

        cart = request.session.get('cart', {})
        product_id = str(product.id)

        current_quantity = cart.get(product_id, 0)

        if current_quantity < product.stock:
            cart[product_id] = current_quantity + 1
            request.session['cart'] = cart
            messages.success(request, f'{product.name} added to cart!')
        else:
            messages.warning(request, 'Available stock limit reached.')

    return redirect('home')
