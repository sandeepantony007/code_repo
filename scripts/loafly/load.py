import time

from loafly.config import (
    API_KEY,
    RETRY_COUNT,
    RETRY_WAIT_SECONDS,
    logger
)

from loafly.gateway import save_to_orders_api


def load(orders):

    for order in orders:

        success = False

        for attempt in range(1, RETRY_COUNT + 1):

            try:

                save_to_orders_api(order, API_KEY)

                logger.info(
                    "Order %s saved successfully.",
                    order["order_id"]
                )

                success = True
                break

            except Exception as e:

                logger.warning(
                    "Attempt %d/%d failed for order %s: %s",
                    attempt,
                    RETRY_COUNT,
                    order["order_id"],
                    e
                )

                if attempt < RETRY_COUNT:
                    time.sleep(RETRY_WAIT_SECONDS)

        if not success:

            logger.error(
                "Giving up on order %s after %d attempts.",
                order["order_id"],
                RETRY_COUNT
            )