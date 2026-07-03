# loafly/models.py

from loafly.config import logger


def clean_price(text):
    if text is None or text.strip() == "":
        raise ValueError("Price is missing.")

    return float(text.replace(",", "").strip())


class Order:

    def __init__(self, order_id, customer):
        self.order_id = order_id
        self.customer = customer
        self.items = []

    def add_item(self, item_name, item_price):
        self.items.append((item_name, item_price))

    def total(self):

        total = 0

        for item_name, price in self.items:

            try:
                total += clean_price(price)

            except ValueError as e:
                logger.warning(
                    "Skipping item '%s' in order %s: %s",
                    item_name,
                    self.order_id,
                    e
                )

            finally:
                logger.info(
                    "Finished processing item '%s' for order %s",
                    item_name,
                    self.order_id
                )

        return total