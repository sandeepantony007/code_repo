"""
legacy_orders.py  -  Loafly's "it ran fine on my laptop" script.

This is the BEFORE. It works for the happy rows, but look at the problems:
  - the price cleaning is copy-pasted inline
  - the discount is a magic number typed into the logic
  - the API key is sitting right here in the code
  - it uses print(), has no error handling, and no retry
  - everything lives in one file

It also crashes the first time it meets an order with a missing price,
which is exactly the kind of 2am breakage this session is about.

Run:  python legacy_orders.py
"""
import csv

#Creating a function to """Turn a price written as text, like '1,250', into a number 1250.0."""
def clean_price(text):
    """
    Convert a price like '1,250' into 1250.0.
    Raises ValueError if price is missing or invalid.
    """
    if text is None or text.strip() == "":
        raise ValueError("Price is missing.")
    
    return float(text.replace(",", "").strip())
    
    
#Creating a function to apply discount
def apply_discount(price, percent):
    return price - (price * percent/100)
    
 
# ---------------- Order Class ---------------- #

class Order:
    def __init__(self, order_id, customer):
        self.order_id = order_id
        self.customer = customer
        self.items = []

    def add_item(self, item_name, item_price):
        """Add an item to the order."""
        self.items.append((item_name, item_price))

    def total(self):
        """Calculate the total order amount."""
        total = 0

        for _, price in self.items:
            total += clean_price(price)

        return total
        
            

# read today's raw orders
rows = []
with open("raw_orders.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        rows.append(row)

# ---------------- Build Order Objects ---------------- #

orders = {}

for row in rows:
    oid = row["order_id"]

    if oid not in orders:
        orders[oid] = Order(
            order_id=oid,
            customer=row["customer"]
        )

    orders[oid].add_item(
        row["item_name"],
        row["item_price"]
    )

# process every order
for order in orders.values():
    total = order.total()
    total = apply_discount(total, 10)
    
    api_key = "loafly-prod-key-9f3a21"                   # secret, sitting in the code (!)
    print("saving order", oid, "for", o["customer"], "total", total)   # no logging, no retry
