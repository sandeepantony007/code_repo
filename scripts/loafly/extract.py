import csv
from loafly.config import INPUT_FILE


def extract():
    """Read raw order data."""

    with open(INPUT_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))