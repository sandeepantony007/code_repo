from loafly.extract import extract
from loafly.transform import transform
from loafly.load import load
from loafly.config import logger


def main():

    logger.info("Pipeline started")

    rows = extract()

    orders = transform(rows)

    load(orders)

    logger.info("Pipeline finished")


if __name__ == "__main__":
    main()