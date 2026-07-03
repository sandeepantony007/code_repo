from loafly.config import DISCOUNT_PERCENT
from loafly.models import Order


def apply_discount(amount):
    return amount - (amount * DISCOUNT_PERCENT / 100)


def transform(rows):

    orders = {}

    for row in rows:
        oid = row["order_id"]

        if oid not in orders:
            orders[oid] = Order(
                oid,
                row["customer"]
            )

        orders[oid].add_item(
            row["item_name"],
            row["item_price"]
        )

    transformed_orders = []

    for order in orders.values():
        transformed_orders.append(
            {
                "order_id": order.order_id,
                "customer": order.customer,
                "total": apply_discount(order.total())
            }
        )

    return transformed_orders