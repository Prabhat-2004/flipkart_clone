
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    PAYMENT_CHOICES = [
        ("cod", "Cash on Delivery"),
        ("upi", "UPI - Demo"),
        ("card", "Card - Demo"),
    ]

    customer_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    delivery_address = models.TextField()

    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    latitude = models.CharField(max_length=50, blank=True)
    longitude = models.CharField(max_length=50, blank=True)

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES
    )
    payment_status = models.CharField(
        max_length=30,
        default="Pending"
    )
    order_status = models.CharField(
        max_length=30,
        default="Placed"
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
