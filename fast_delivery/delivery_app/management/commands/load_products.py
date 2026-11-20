
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction

from delivery_app.models import Category, Product


PRODUCTS = {
    "Fruits & Vegetables": [
        ("Apple", "180", 30),
        ("Banana", "60", 40),
        ("Orange", "90", 35),
        ("Mango", "120", 25),
        ("Potato", "35", 50),
        ("Onion", "40", 50),
        ("Tomato", "30", 45),
        ("Carrot", "50", 30),
        ("Broccoli", "80", 20),
        ("Green Chilli", "25", 30),
    ],

    "Dairy & Breakfast": [
        ("Full Cream Milk 1L", "68", 40),
        (" toned Milk 1L", "58", 35),
        ("Butter 500g", "280", 20),
        ("Cheese Slices", "125", 25),
        ("Paneer 200g", "95", 25),
        ("Curd 500g", "45", 30),
        ("Eggs 12 Pieces", "90", 40),
        ("Corn Flakes 500g", "180", 20),
        ("Oats 1kg", "160", 25),
        ("Ghee 500ml", "310", 15),
    ],

    "Snacks & Munchies": [
        ("Salted Potato Chips", "20", 100),
        ("Masala Chips", "20", 100),
        ("Cheese Balls", "35", 50),
        ("Nachos", "50", 40),
        ("Popcorn", "30", 50),
        ("Peanuts 200g", "55", 30),
        ("Roasted Cashews 200g", "220", 20),
        ("Chocolate Bar", "40", 60),
        ("Cream Biscuits", "30", 60),
        ("Mixed Namkeen 400g", "95", 30),
    ],

    "Cold Drinks & Juices": [
        ("Cola 750ml", "40", 40),
        ("Lemon Soda 750ml", "40", 35),
        ("Orange Juice 1L", "120", 25),
        ("Mango Juice 1L", "110", 25),
        ("Mineral Water 1L", "20", 100),
        ("Energy Drink", "110", 30),
        ("Iced Tea 500ml", "45", 30),
        ("Coconut Water", "45", 30),
    ],

    "Bakery & Biscuits": [
        ("White Bread", "40", 30),
        ("Brown Bread", "50", 25),
        ("Burger Buns", "35", 20),
        ("Chocolate Cake", "250", 10),
        ("Vanilla Muffins", "80", 20),
        ("Digestive Biscuits", "45", 40),
        ("Cookies Pack", "60", 35),
        ("Rusk Toast", "50", 30),
    ],

    "Personal Care": [
        ("Bathing Soap Pack", "120", 40),
        ("Shampoo 340ml", "220", 25),
        ("Toothpaste", "95", 40),
        ("Toothbrush Pack", "80", 30),
        ("Face Wash", "160", 25),
        ("Body Lotion", "190", 20),
        ("Hand Wash", "99", 30),
        ("Deodorant", "180", 20),
    ],

    "Home Care": [
        ("Detergent Powder 1kg", "120", 35),
        ("Dishwash Liquid", "110", 30),
        ("Floor Cleaner 1L", "145", 25),
        ("Toilet Cleaner", "95", 30),
        ("Garbage Bags", "70", 30),
        ("Kitchen Cleaning Sponge", "35", 40),
        ("Room Freshener", "160", 20),
        ("Laundry Liquid", "190", 20),
    ],

    "Atta, Rice & Dal": [
        ("Wheat Atta 5kg", "250", 30),
        ("Basmati Rice 5kg", "450", 20),
        ("Regular Rice 5kg", "280", 25),
        ("Toor Dal 1kg", "160", 30),
        ("Moong Dal 1kg", "140", 30),
        ("Chana Dal 1kg", "110", 30),
        ("Besan 1kg", "95", 25),
        ("Sooji 1kg", "55", 25),
    ],

    "Instant Food": [
        ("Instant Noodles Pack", "15", 100),
        ("Cup Noodles", "55", 40),
        ("Pasta 500g", "75", 30),
        ("Macaroni 500g", "65", 25),
        ("Instant Poha", "45", 30),
        ("Instant Upma", "50", 25),
        ("Ready Mix Dosa", "90", 20),
        ("Soup Pack", "35", 30),
    ],

    "Baby Care": [
        ("Baby Diapers Small Pack", "250", 20),
        ("Baby Wipes", "120", 25),
        ("Baby Shampoo", "180", 20),
        ("Baby Lotion", "160", 20),
        ("Baby Soap", "90", 25),
        ("Baby Powder", "130", 20),
    ],

    "Mobiles & Electronics": [
        ("Android Smartphone", "12999", 10),
        ("Budget Smartphone", "7999", 12),
        ("Bluetooth Earbuds", "999", 20),
        ("Wireless Headphones", "1499", 15),
        ("Power Bank 10000mAh", "899", 20),
        ("USB Type-C Cable", "199", 40),
        ("Fast Charger", "499", 25),
        ("Bluetooth Speaker", "1299", 15),
        ("Smart Watch", "1799", 15),
        ("Computer Mouse", "399", 25),
    ],

    "Fashion": [
        ("Men's Casual T-Shirt", "499", 20),
        ("Men's Jeans", "999", 15),
        ("Women's Kurti", "699", 20),
        ("Women's Top", "549", 20),
        ("Sports Shoes", "1499", 15),
        ("Casual Shoes", "1199", 15),
        ("Men's Wallet", "399", 25),
        ("Backpack", "899", 20),
    ],

    "Home & Kitchen": [
        ("Stainless Steel Water Bottle", "299", 30),
        ("Non Stick Frying Pan", "699", 15),
        ("Dinner Plate Set", "499", 15),
        ("Electric Kettle", "999", 15),
        ("Mixer Grinder", "2499", 10),
        ("Storage Container Set", "399", 20),
        ("Bedsheet Double", "799", 15),
        ("LED Desk Lamp", "599", 20),
    ],

    "Books & Stationery": [
        ("Notebook Pack", "120", 40),
        ("Ball Pen Pack", "60", 50),
        ("Drawing Book", "75", 30),
        ("School Geometry Box", "110", 25),
        ("Office File Pack", "90", 30),
        ("Sticky Notes Pack", "55", 30),
        ("Color Pencils", "95", 25),
        ("Desk Organizer", "199", 20),
    ],

    "Sports & Fitness": [
        ("Cricket Tennis Ball", "80", 30),
        ("Football", "499", 15),
        ("Badminton Racket", "599", 15),
        ("Yoga Mat", "499", 20),
        ("Skipping Rope", "149", 30),
        ("Dumbbell Pair", "899", 10),
        ("Water Bottle Sports", "249", 25),
        ("Resistance Band", "299", 20),
    ],
}


class Command(BaseCommand):
    help = "Load demo grocery and ecommerce products"

    @transaction.atomic
    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for category_name, items in PRODUCTS.items():
            category, _ = Category.objects.get_or_create(
                name=category_name
            )

            for index, (name, price, stock) in enumerate(items):
                original_price = Decimal(price)

                # Give selected products a 10% demo discount.
                discount_price = None
                if index % 4 != 0:
                    discount_price = (
                        original_price * Decimal("0.90")
                    ).quantize(Decimal("0.01"))

                product, created = Product.objects.update_or_create(
                    category=category,
                    name=name,
                    defaults={
                        "description": (
                            f"{name} - quality demo product "
                            "available at Fast Delivery."
                        ),
                        "price": original_price,
                        "discount_price": discount_price,
                        "stock": stock,
                        "is_available": True,
                    },
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Product loading complete! "
                f"Created: {created_count}, Updated: {updated_count}"
            )
        )

