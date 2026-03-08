# frozenset_bundles.py
# Bundle Discount System using frozensets
# Part B — Stretch Problem

import timeit

"""
=============================================================
RESEARCH: frozenset vs set
=============================================================

What is frozenset?
    A frozenset is an immutable version of a Python set.
    Once created it cannot be modified — you cannot add,
    remove, or update its elements.

Difference between set and frozenset:
    set:
        - Mutable: supports add(), remove(), discard(), pop()
        - Cannot be used as a dictionary key
        - Cannot be placed inside another set
        - Created with set() or {1, 2, 3}

    frozenset:
        - Immutable: no add/remove methods
        - Can be used as a dictionary key (it is hashable)
        - Can be an element inside another set
        - Created with frozenset({1, 2, 3})

When to use frozenset in real systems:
    1. Bundle keys in dictionaries (like this file) — you
       need an unordered group of categories as a stable key.
    2. Caching and memoization — frozensets can be hashed,
       so they work as keys in LRU cache lookups.
    3. Graph algorithms — representing edges as frozensets
       so {A, B} and {B, A} are the same edge.
    4. Config flags — a fixed set of feature flags that
       should never change at runtime.
=============================================================
"""

# ─── 2. Bundle Discount Dictionary ────────────────────────────────────────────
# Keys are frozensets of category names; values are discount %
bundle_discounts = {
    frozenset({"Electronics", "Books"}):   10,   # 10% off
    frozenset({"Clothing", "Home"}):       15,   # 15% off
    frozenset({"Electronics", "Clothing"}): 8,   # 8% off
    frozenset({"Books", "Home"}):          12,   # 12% off
    frozenset({"Electronics", "Books", "Clothing"}): 20,  # 20% off
}

# ─── 3. Bundle Checker Function ───────────────────────────────────────────────
def check_bundle_discount(cart):
    """
    Given a cart (list/set of Product namedtuples), find the highest
    applicable bundle discount based on the categories present.

    Args:
        cart: iterable of Product namedtuples
    Returns:
        tuple (discount_percent, matched_bundle) or (0, None)
    """
    cart_categories = frozenset(p.category for p in cart)

    best_discount = 0
    best_bundle   = None

    for bundle, discount in bundle_discounts.items():
        # bundle matches if ALL its required categories are in the cart
        if bundle.issubset(cart_categories):
            if discount > best_discount:
                best_discount = discount
                best_bundle   = bundle

    return best_discount, best_bundle


# ─── 4. Performance Benchmark: set vs frozenset ───────────────────────────────
ITERATIONS = 100_000

set_time = timeit.timeit(
    stmt="s = {1, 2, 3, 4, 5}",
    number=ITERATIONS
)

frozenset_time = timeit.timeit(
    stmt="fs = frozenset({1, 2, 3, 4, 5})",
    number=ITERATIONS
)

"""
Benchmark Results (100,000 iterations, approximate):
------------------------------------------------------
set creation:       ~0.006 – 0.010 seconds
frozenset creation: ~0.010 – 0.016 seconds

frozenset is slightly slower to create because Python
needs to freeze (hash) the structure at creation time.
However, frozenset lookup in dictionaries is O(1) just
like regular sets, and it provides the added benefit of
being usable as a dictionary key.

Conclusion: use frozenset when you need immutability
or dictionary/set membership of a set-like object; use
regular set when you need to modify contents dynamically.
"""


# ─── Main Demo ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # import catalog for demo
    from product_analytics import (
        customer_1_cart, customer_2_cart, customer_3_cart,
        customer_4_cart, customer_5_cart
    )

    print("=" * 55)
    print("        Bundle Discount Checker")
    print("=" * 55)

    demo_carts = {
        "Customer 1": customer_1_cart,
        "Customer 2": customer_2_cart,
        "Customer 3": customer_3_cart,
        "Customer 4": customer_4_cart,
        "Customer 5": customer_5_cart,
    }

    for name, cart in demo_carts.items():
        cats = {p.category for p in cart}
        discount, bundle = check_bundle_discount(cart)
        print(f"\n  {name} | Categories: {cats}")
        if discount > 0:
            print(f"    Bundle matched: {set(bundle)}")
            print(f"    Discount applied: {discount}%")
        else:
            print("    No bundle discount applicable.")

    print("\n" + "=" * 55)
    print("  Performance Benchmark (100,000 iterations)")
    print("=" * 55)
    print(f"  set creation time      : {set_time:.4f} seconds")
    print(f"  frozenset creation time: {frozenset_time:.4f} seconds")
    diff = ((frozenset_time - set_time) / set_time) * 100
    print(f"  frozenset is ~{abs(diff):.1f}% {'slower' if diff > 0 else 'faster'} than set")
    print("=" * 55)
