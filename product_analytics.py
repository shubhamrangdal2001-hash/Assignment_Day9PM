# product_analytics.py
# E-commerce Product Analytics Tool
# Uses tuples and sets to analyze shopping behaviour

from collections import namedtuple

# ─── 1. Named Tuple Definition ────────────────────────────────────────────────
Product = namedtuple("Product", ["id", "name", "category", "price"])

# ─── 2. Product Catalog (15 products across 4 categories) ─────────────────────
catalog = [
    # Electronics
    Product(1,  "Laptop",           "Electronics", 75000),
    Product(2,  "Smartphone",       "Electronics", 45000),
    Product(3,  "Wireless Earbuds", "Electronics", 3500),
    Product(4,  "Smart Watch",      "Electronics", 18000),
    Product(5,  "Tablet",           "Electronics", 32000),

    # Clothing
    Product(6,  "Denim Jacket",     "Clothing",    2200),
    Product(7,  "Running Shoes",    "Clothing",    3800),
    Product(8,  "Cotton T-Shirt",   "Clothing",    699),
    Product(9,  "Formal Trousers",  "Clothing",    1500),

    # Books
    Product(10, "Clean Code",       "Books",       650),
    Product(11, "Python Crash Course", "Books",    499),
    Product(12, "Atomic Habits",    "Books",       399),

    # Home
    Product(13, "Air Purifier",     "Home",        8500),
    Product(14, "Coffee Maker",     "Home",        3200),
    Product(15, "Desk Lamp",        "Home",        1100),
]

# shorthand references for building carts
p1, p2, p3, p4, p5 = catalog[0], catalog[1], catalog[2], catalog[3], catalog[4]
p6, p7, p8, p9     = catalog[5], catalog[6], catalog[7], catalog[8]
p10, p11, p12      = catalog[9], catalog[10], catalog[11]
p13, p14, p15      = catalog[12], catalog[13], catalog[14]

# ─── 3. Customer Carts (sets of Product namedtuples) ──────────────────────────
customer_1_cart = {p1, p3, p10, p11, p14}
customer_2_cart = {p2, p3, p10, p7,  p13}
customer_3_cart = {p3, p5, p10, p12, p15}
customer_4_cart = {p3, p4, p10, p8,  p14}
customer_5_cart = {p3, p6, p10, p11, p13}

all_carts = [customer_1_cart, customer_2_cart, customer_3_cart,
             customer_4_cart, customer_5_cart]

# ─── 4. Shopping Behaviour Analysis ──────────────────────────────────────────

# (a) Bestsellers — products in ALL carts (set intersection)
def get_bestsellers(carts):
    result = carts[0].copy()
    for cart in carts[1:]:
        result = result & cart          # intersection
    return result

# (b) Catalog Reach — products appearing in ANY cart (set union)
def get_catalog_reach(carts):
    result = set()
    for cart in carts:
        result = result | cart          # union
    return result

# (c) Exclusive Purchases — what only customer_1 bought
def get_exclusive_purchases(target_cart, other_carts):
    others_combined = set()
    for cart in other_carts:
        others_combined = others_combined | cart
    return target_cart - others_combined   # set difference

# ─── 5. Product Recommendation ────────────────────────────────────────────────
def recommend_products(customer_cart, all_carts):
    """
    Suggest products other customers bought that this customer hasn't seen.
    Uses set difference: (union of all others) - this customer's cart.
    """
    other_products = set()
    for cart in all_carts:
        if cart != customer_cart:
            other_products = other_products | cart
    recommendations = other_products - customer_cart
    return recommendations

# ─── 6. Category Summary ──────────────────────────────────────────────────────
def category_summary():
    """
    Returns a dict mapping category -> set of product names in that category.
    Uses set comprehension.
    """
    categories = {p.category for p in catalog}   # all unique categories
    summary = {
        cat: {p.name for p in catalog if p.category == cat}
        for cat in categories
    }
    return summary

# ─── Main: Print results ──────────────────────────────────────────────────────
if __name__ == "__main__":

    print("=" * 55)
    print("        E-Commerce Product Analytics Tool")
    print("=" * 55)

    # Bestsellers
    bestsellers = get_bestsellers(all_carts)
    print("\n[Bestsellers] Products in ALL 5 carts:")
    for p in bestsellers:
        print(f"  - {p.name} ({p.category}) | Rs. {p.price}")

    # Catalog Reach
    reached = get_catalog_reach(all_carts)
    print(f"\n[Catalog Reach] Products appearing in ANY cart: {len(reached)}")
    for p in sorted(reached, key=lambda x: x.id):
        print(f"  - {p.name}")

    # Exclusive Purchases (customer 1)
    others = all_carts[1:]
    exclusive = get_exclusive_purchases(customer_1_cart, others)
    print("\n[Exclusive Purchases] Only Customer 1 bought:")
    if exclusive:
        for p in exclusive:
            print(f"  - {p.name}")
    else:
        print("  (none — all items also bought by others)")

    # Recommendations for Customer 1
    recs = recommend_products(customer_1_cart, all_carts)
    print("\n[Recommendations] Customer 1 might also like:")
    for p in sorted(recs, key=lambda x: x.id):
        print(f"  - {p.name} (Rs. {p.price})")

    # Category Summary
    print("\n[Category Summary]")
    summary = category_summary()
    for cat, names in sorted(summary.items()):
        print(f"  {cat}: {names}")

    print("\n" + "=" * 55)
