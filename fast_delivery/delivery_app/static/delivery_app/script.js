
document.addEventListener("DOMContentLoaded", function () {

    // 3D-style category illustrations
    const categoryIcons = {
        "fruits & vegetables": "🍎",
        "dairy & breakfast": "🥛",
        "snacks & munchies": "🍿",
        "cold drinks & juices": "🥤",
        "bakery & biscuits": "🍞",
        "personal care": "🧴",
        "home care": "🧹",
        "atta, rice & dal": "🍚",
        "instant food": "🍜",
        "baby care": "🍼",
        "mobiles & electronics": "📱",
        "fashion": "👟",
        "home & kitchen": "🍳",
        "books & stationery": "📚",
        "sports & fitness": "⚽"
    };

    document.querySelectorAll(".category-art").forEach(function (element) {
        const category = element.dataset.category.toLowerCase().trim();
        const icon = categoryIcons[category] || "🛍️";
        element.querySelector(".category-emoji").textContent = icon;
    });

    // Product illustrations
    const productIcons = [
        [/apple/i, "🍎"],
        [/banana/i, "🍌"],
        [/orange/i, "🍊"],
        [/mango/i, "🥭"],
        [/potato/i, "🥔"],
        [/onion/i, "🧅"],
        [/tomato/i, "🍅"],
        [/carrot/i, "🥕"],
        [/broccoli/i, "🥦"],
        [/chilli/i, "🌶️"],
        [/milk/i, "🥛"],
        [/butter/i, "🧈"],
        [/cheese|paneer/i, "🧀"],
        [/curd|yogurt/i, "🥣"],
        [/egg/i, "🥚"],
        [/oats|corn flakes/i, "🥣"],
        [/ghee/i, "🫙"],
        [/chips|nachos/i, "🍟"],
        [/popcorn/i, "🍿"],
        [/peanuts|cashews/i, "🥜"],
        [/chocolate/i, "🍫"],
        [/namkeen/i, "🥨"],
        [/juice/i, "🧃"],
        [/cola|soda|drink|water/i, "🥤"],
        [/tea/i, "🫖"],
        [/bread/i, "🍞"],
        [/cake|muffin/i, "🧁"],
        [/biscuit|cookie/i, "🍪"],
        [/rusk/i, "🥖"],
        [/soap/i, "🧼"],
        [/shampoo|lotion|face wash|deodorant/i, "🧴"],
        [/toothpaste|toothbrush/i, "🪥"],
        [/detergent|cleaner|dishwash/i, "🧽"],
        [/garbage bag/i, "🗑️"],
        [/atta|wheat|flour/i, "🌾"],
        [/rice|dal|sooji|besan/i, "🍚"],
        [/noodles|pasta|macaroni|upma|poha/i, "🍜"],
        [/soup/i, "🥣"],
        [/baby|diaper/i, "🍼"],
        [/smartphone|phone/i, "📱"],
        [/earbud|headphone/i, "🎧"],
        [/power bank/i, "🔋"],
        [/charger|cable/i, "🔌"],
        [/speaker/i, "🔊"],
        [/watch/i, "⌚"],
        [/mouse/i, "🖱️"],
        [/t-shirt|shirt|top|kurti/i, "👕"],
        [/jeans/i, "👖"],
        [/shoe|sneaker/i, "👟"],
        [/wallet/i, "👛"],
        [/backpack|bag/i, "🎒"],
        [/bottle/i, "🚰"],
        [/pan|cooker|kettle|mixer/i, "🍳"],
        [/plate|container/i, "🥣"],
        [/bedsheet/i, "🛏️"],
        [/lamp/i, "💡"],
        [/notebook|book/i, "📚"],
        [/pen|pencil/i, "✏️"],
        [/geometry|stationery/i, "📐"],
        [/cricket|ball/i, "🏏"],
        [/football/i, "⚽"],
        [/badminton|racket/i, "🏸"],
        [/yoga|mat/i, "🧘"],
        [/dumbbell/i, "🏋️"],
        [/rope/i, "🪢"],
        [/band/i, "💪"]
    ];

    document.querySelectorAll(".product-art").forEach(function (element) {
        const name = element.dataset.name || "";
        const category = (element.dataset.category || "").toLowerCase();

        let icon = "🛍️";

        for (const [pattern, emoji] of productIcons) {
            if (pattern.test(name)) {
                icon = emoji;
                break;
            }
        }

        if (icon === "🛍️") {
            if (category.includes("fruit")) icon = "🍎";
            else if (category.includes("dairy")) icon = "🥛";
            else if (category.includes("snack")) icon = "🍿";
            else if (category.includes("drink")) icon = "🥤";
            else if (category.includes("bakery")) icon = "🍞";
            else if (category.includes("care")) icon = "🧴";
            else if (category.includes("rice")) icon = "🍚";
            else if (category.includes("instant")) icon = "🍜";
            else if (category.includes("mobile")) icon = "📱";
            else if (category.includes("fashion")) icon = "👕";
            else if (category.includes("kitchen")) icon = "🍳";
            else if (category.includes("book")) icon = "📚";
            else if (category.includes("sport")) icon = "⚽";
        }

        element.querySelector(".product-emoji").textContent = icon;
    });

    // Fade out Django messages
    const messages = document.querySelector(".messages");

    if (messages) {
        setTimeout(function () {
            messages.style.transition = "opacity .5s";
            messages.style.opacity = "0";

            setTimeout(function () {
                messages.remove();
            }, 500);
        }, 3500);
    }

});
