import os
import logging

from dotenv import load_dotenv

load_dotenv()

INPUT_FILE = "raw_orders.csv"
DISCOUNT_PERCENT = 10
CURRENCY = "USD"
RETRY_COUNT = 3
RETRY_WAIT_SECONDS = 2

API_KEY = os.getenv("LOAFLY_API_KEY")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler("loafly.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)