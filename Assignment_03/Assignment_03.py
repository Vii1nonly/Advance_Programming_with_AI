"""
================================================================================
 Assignment 03 — Refactor the Messy Store System
 192-201 Advanced Computer Programming with Generative AI
 Week 5 — OOP Design & Refactoring   |   Faculty of IT (International), Siam University
 Lecturer: Hrang Kap Lian
================================================================================

 Maps to: CLO1 (object-oriented design) and CLO5 (responsible, verified AI use)
 Weight:  10 Points     AI-use level: Level 2 (AI-assisted + PROMPT LOG required)

--------------------------------------------------------------------------------
 THE TASK
--------------------------------------------------------------------------------
 You are given ONE working program that is badly written. Do NOT add features and
 do NOT change what it does. REFACTOR it: reshape the code into a clean,
 object-oriented design while producing the EXACT SAME output.

   The one rule of refactoring:  same behaviour, cleaner code.
   If the output changes, it is no longer a refactor — it is a bug.

 How to run:
   python Assignment_03.py
 It prints PASS when your refactor reproduces the original output exactly,
 or FAIL with the first line that differs.

--------------------------------------------------------------------------------
 WHAT YOU WILL PRACTISE (use ALL of these)
--------------------------------------------------------------------------------
   Week 2  Model data as CLASSES with attributes and methods (not tuples/lists).
   Week 3  ENCAPSULATION — validate object state in the constructor.
   Week 4  INHERITANCE & POLYMORPHISM — replace the `if tier == ...` chains
           with a family of classes.
   Week 5  COMPOSITION (has-a) — an Order has-a customer and has-many items;
           an item has-a product.
   Week 5  PURE FUNCTIONS vs MODIFIERS — calculation methods RETURN values and
           print nothing; keep them separate from the receipt printing.
   Week 5  INTERFACE vs IMPLEMENTATION — separate WHAT the receipt shows from
           HOW the totals are computed.

--------------------------------------------------------------------------------
 RULES
--------------------------------------------------------------------------------
 1. Behaviour must stay identical — the self-test must print PASS.
 2. Refactor only. No new discounts, no prettier receipts, no extra products.
 3. You choose the class design — there is no single correct answer.
 4. Level-2 AI use: you may use AI to explain/suggest/refactor, but YOU verify
    every change and you keep a PROMPT LOG (in CHANGES.md).
 5. Work in small steps: change one thing -> run -> keep it green.

--------------------------------------------------------------------------------
 THE SCENARIO
--------------------------------------------------------------------------------
 A small online store prints a receipt per order and a grand total. Business rules:
   - Tax: electronics & stationery = 7%; food = tax-free.
   - Membership discount on the subtotal:
         tier      subtotal<=100   subtotal>100
         none        0%              0%
         silver      2%              5%
         gold        5%              10%
         platinum    10%             15%
   - Bulk discount: 10+ items in total -> add another 3% of the subtotal.
   - total = subtotal - discount + tax
   - points = int(total // 10) * tier_multiplier   (none x1, silver x2, gold x3, platinum x5)
 You do not change these rules — you express them cleanly.

--------------------------------------------------------------------------------
 YOUR TASKS  (see the rubric at the bottom)
--------------------------------------------------------------------------------
   A. (required) Model the domain with classes + composition
                 e.g. Product, OrderItem (has-a Product), Customer, Order.
   B. (required) Encapsulate & validate state in constructors (e.g. qty >= 1).
   C. (required) Replace the tier `if/elif` chains (discount AND points) with
                 polymorphism — a class family, no `if tier == ...`.
   D. (required) Separate calculation from printing: pure methods return numbers.
   E. (required) Kill magic numbers (name them) and remove the leftover `global`.
   F. (stretch)  Let each product decide its own tax — no `if category` in totals.
   G. (stretch)  Add a sensible __str__ where it helps.

--------------------------------------------------------------------------------
 SUBMIT
--------------------------------------------------------------------------------
   1) This file, Assignment_03.py, with your refactor (self-test prints PASS).
   2) CHANGES.md — your written explanation of each change + your prompt log.
================================================================================
"""

import io
import contextlib


# ==============================================================================
#  LEGACY STORE SYSTEM  —  messy but working.   DO NOT EDIT THIS SECTION.
#  Read it, understand it, and use its output as the correct behaviour.
# ==============================================================================
PRODUCTS = [
    ("Laptop", 1200.0, "electronics"),
    ("Headphones", 200.0, "electronics"),
    ("Coffee Beans", 15.0, "food"),
    ("Notebook", 5.0, "stationery"),
    ("Water Bottle", 10.0, "food"),
    ("Monitor", 300.0, "electronics"),
    ("Pen", 2.0, "stationery"),
]
TAXRATE = 0.07
foodtax = 0.0
ORDERS = [
    ("Alice", "gold", [(0, 1), (1, 2), (2, 3)]),
    ("Bob", "none", [(3, 10), (6, 5)]),
    ("Charlie", "platinum", [(5, 2), (4, 6), (2, 2)]),
    ("Dana", "silver", [(1, 1), (3, 3), (6, 10)]),
]


def calc(o):
    global TAXRATE
    n = o[0]; t = o[1]; items = o[2]
    sub = 0.0; tax = 0.0
    print("Receipt for " + n + " (" + t + ")")
    print("-" * 40)
    for it in items:
        pi = it[0]; q = it[1]
        p = PRODUCTS[pi][1]; nm = PRODUCTS[pi][0]; cat = PRODUCTS[pi][2]
        line = p * q
        sub = sub + line
        if cat == "food":
            tax = tax + line * foodtax
        else:
            tax = tax + line * TAXRATE
        print(nm + " x" + str(q) + " = " + str(line))
    d = 0.0
    if t == "none":
        d = 0.0
    elif t == "silver":
        if sub > 100: d = sub * 0.05
        else: d = sub * 0.02
    elif t == "gold":
        if sub > 100: d = sub * 0.10
        else: d = sub * 0.05
    elif t == "platinum":
        if sub > 100: d = sub * 0.15
        else: d = sub * 0.10
    totalqty = 0
    for it in items:
        totalqty = totalqty + it[1]
    if totalqty >= 10:
        d = d + sub * 0.03
    total = sub - d + tax
    pts = 0
    if t == "none": pts = int(total // 10)
    elif t == "silver": pts = int(total // 10) * 2
    elif t == "gold": pts = int(total // 10) * 3
    elif t == "platinum": pts = int(total // 10) * 5
    print("-" * 40)
    print("Subtotal: " + str(round(sub, 2)))
    print("Discount: " + str(round(d, 2)))
    print("Tax: " + str(round(tax, 2)))
    print("Total: " + str(round(total, 2)))
    print("Points earned: " + str(pts))
    print("")
    return total


def legacy_main():
    grand = 0.0
    for o in ORDERS:
        grand = grand + calc(o)
    print("GRAND TOTAL (all orders): " + str(round(grand, 2)))


# ==============================================================================
#  BEHAVIOUR LOCK  —  DO NOT EDIT.
#  Captures the exact output of the legacy program as the target you must match.
# ==============================================================================
def capture(fn):
    """Run fn() and return everything it printed, as a string."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn()
    return buf.getvalue()


GOLDEN_OUTPUT = capture(legacy_main)


# ==============================================================================
#  YOUR REFACTORED SOLUTION  —  WRITE YOUR CODE BELOW.
#  Design your own classes. A suggested skeleton is commented out — change freely.
#  Your program must define refactored_main() which PRINTS the same output.
# ==============================================================================

# --- named constants (replace the magic numbers) ---
STANDARD_TAX_RATE  = 0.07     # electronics & stationery
FOOD_TAX_RATE      = 0.0      # food is tax-free
TAX_RATE_BY_CATEGORY = {
    "electronics": STANDARD_TAX_RATE,
    "stationery":  STANDARD_TAX_RATE,
    "food":        FOOD_TAX_RATE,
}
DISCOUNT_THRESHOLD = 100      # subtotal ABOVE this gets the larger tier discount
BULK_QTY_THRESHOLD = 10       # this many items or more earns the bulk discount
BULK_DISCOUNT_RATE = 0.03
POINTS_DIVISOR     = 10       # 1 point per 10 spent, before the tier multiplier
RECEIPT_RULE       = "-" * 40


def money(amount):
    """Format an amount exactly as the legacy receipt did (e.g. 1645.0, 16.45)."""
    return str(round(amount, 2))


# --- domain classes ---
class Product:
    """A catalogue product. Each product knows its own tax rate (task F)."""

    def __init__(self, name, price, category):
        if not isinstance(name, str) or not name:
            raise ValueError("Product name must be a non-empty string")
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError(f"Price of {name} must be a number >= 0")
        if category not in TAX_RATE_BY_CATEGORY:
            raise ValueError(f"Unknown category for {name}: {category!r}")
        self.name = name
        self.price = float(price)
        self.category = category

    def tax_rate(self):
        return TAX_RATE_BY_CATEGORY[self.category]


class OrderItem:
    """One line of an order: has-a Product, plus a quantity."""

    def __init__(self, product, quantity):
        if not isinstance(product, Product):
            raise TypeError("OrderItem needs a Product")
        if not isinstance(quantity, int) or quantity < 1:
            raise ValueError(f"Quantity of {product.name} must be a whole number >= 1")
        self.product = product
        self.quantity = quantity

    def line_total(self):
        return self.product.price * self.quantity

    def tax(self):
        return self.line_total() * self.product.tax_rate()

    def __str__(self):
        return f"{self.product.name} x{self.quantity} = {self.line_total()}"


class Customer:
    """A customer with no membership. Subclasses override the tier values."""
    tier_name = "none"
    small_order_rate = 0.0     # discount rate when subtotal <= DISCOUNT_THRESHOLD
    large_order_rate = 0.0     # discount rate when subtotal >  DISCOUNT_THRESHOLD
    points_multiplier = 1

    def __init__(self, name):
        if not isinstance(name, str) or not name:
            raise ValueError("Customer name must be a non-empty string")
        self.name = name

    def discount_rate(self, subtotal):
        if subtotal > DISCOUNT_THRESHOLD:
            return self.large_order_rate
        return self.small_order_rate

    def __str__(self):
        return f"{self.name} ({self.tier_name})"


class SilverCustomer(Customer):
    tier_name = "silver"
    small_order_rate = 0.02
    large_order_rate = 0.05
    points_multiplier = 2


class GoldCustomer(Customer):
    tier_name = "gold"
    small_order_rate = 0.05
    large_order_rate = 0.10
    points_multiplier = 3


class PlatinumCustomer(Customer):
    tier_name = "platinum"
    small_order_rate = 0.10
    large_order_rate = 0.15
    points_multiplier = 5


class Order:
    """An order: has-a Customer and has-many OrderItems.
    The calculation methods are pure - they return numbers and print nothing."""

    def __init__(self, customer, items):
        if not isinstance(customer, Customer):
            raise TypeError("Order needs a Customer")
        if not items or not all(isinstance(item, OrderItem) for item in items):
            raise ValueError("Order needs at least one OrderItem")
        self.customer = customer
        self.items = tuple(items)

    def subtotal(self):
        return sum(item.line_total() for item in self.items)

    def total_quantity(self):
        return sum(item.quantity for item in self.items)

    def discount(self):
        subtotal = self.subtotal()
        discount = subtotal * self.customer.discount_rate(subtotal)
        if self.total_quantity() >= BULK_QTY_THRESHOLD:
            discount += subtotal * BULK_DISCOUNT_RATE
        return discount

    def tax(self):
        return sum(item.tax() for item in self.items)

    def total(self):
        return self.subtotal() - self.discount() + self.tax()

    def points(self):
        return int(self.total() // POINTS_DIVISOR) * self.customer.points_multiplier

    def receipt(self):
        """Build the receipt text. Only lays out results - no calculation here."""
        lines = [f"Receipt for {self.customer}", RECEIPT_RULE]
        lines += [str(item) for item in self.items]
        lines += [
            RECEIPT_RULE,
            f"Subtotal: {money(self.subtotal())}",
            f"Discount: {money(self.discount())}",
            f"Tax: {money(self.tax())}",
            f"Total: {money(self.total())}",
            f"Points earned: {self.points()}",
        ]
        return "\n".join(lines)


# --- store data, as objects ---
LAPTOP       = Product("Laptop", 1200.0, "electronics")
HEADPHONES   = Product("Headphones", 200.0, "electronics")
COFFEE_BEANS = Product("Coffee Beans", 15.0, "food")
NOTEBOOK     = Product("Notebook", 5.0, "stationery")
WATER_BOTTLE = Product("Water Bottle", 10.0, "food")
MONITOR      = Product("Monitor", 300.0, "electronics")
PEN          = Product("Pen", 2.0, "stationery")


def build_orders():
    return [
        Order(GoldCustomer("Alice"),
              [OrderItem(LAPTOP, 1), OrderItem(HEADPHONES, 2), OrderItem(COFFEE_BEANS, 3)]),
        Order(Customer("Bob"),
              [OrderItem(NOTEBOOK, 10), OrderItem(PEN, 5)]),
        Order(PlatinumCustomer("Charlie"),
              [OrderItem(MONITOR, 2), OrderItem(WATER_BOTTLE, 6), OrderItem(COFFEE_BEANS, 2)]),
        Order(SilverCustomer("Dana"),
              [OrderItem(HEADPHONES, 1), OrderItem(NOTEBOOK, 3), OrderItem(PEN, 10)]),
    ]


def refactored_main():
    """Print every receipt and the grand total — same output as legacy_main()."""
    orders = build_orders()
    for order in orders:
        print(order.receipt())
        print()
    grand_total = sum(order.total() for order in orders)
    print("GRAND TOTAL (all orders): " + money(grand_total))


# ==============================================================================
#  SELF-TEST  —  DO NOT EDIT.   Run:  python Assignment_03.py
# ==============================================================================
def _check():
    try:
        your_output = capture(refactored_main)
    except NotImplementedError:
        print("Solution not implemented yet.\n")
        print("Below is the TARGET output your refactor must reproduce exactly:\n")
        print(GOLDEN_OUTPUT)
        return

    if your_output == GOLDEN_OUTPUT:
        print("PASS - behaviour is unchanged. Your refactor is safe.\n")
    else:
        print("FAIL - the output changed, so this is not yet a valid refactor.\n")
        g = GOLDEN_OUTPUT.splitlines()
        y = your_output.splitlines()
        for i in range(max(len(g), len(y))):
            gl = g[i] if i < len(g) else "<no line>"
            yl = y[i] if i < len(y) else "<no line>"
            if gl != yl:
                print("First difference at line " + str(i + 1) + ":")
                print("  expected: " + repr(gl))
                print("  yours:    " + repr(yl))
                break


if __name__ == "__main__":
    _check()


# ==============================================================================
#  RUBRIC (10 pts)
#   Behaviour preserved (self-test PASS) .................. 2
#   Domain modelling & composition ....................... 2
#   Polymorphism (tier discount & points, no if/elif) .... 1.5
#   Pure calculation vs I/O separation ................... 1.5
#   Encapsulation & validation ........................... 1
#   Clean code (names, no magic numbers, DRY, no global).. 1
#   CHANGES.md explanation (per-change, before->after) ...  0.5
#   CHANGES.md prompt log (Level-2) ......................  0.5
#  NOTE: passing the test alone is only 20/100 — most marks are for the DESIGN
#        and for explaining and verifying your changes. 
# ==============================================================================
