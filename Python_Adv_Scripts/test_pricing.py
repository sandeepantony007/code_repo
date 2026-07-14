import pytest

from pricing import (
    member_price,
    add_gst,
    delivery_fee,
    loyalty_points
)


# -------------------------------------------------
# Tests for member_price()
# -------------------------------------------------

def test_member_price_normal_discount():
    """
    10% member discount on 1000 should return 900
    """
    assert member_price(1000, 10) == 900


def test_member_price_zero_discount():
    """
    Edge case:
    0% discount should return original price
    """
    assert member_price(1000, 0) == 1000


def test_member_price_full_discount():
    """
    Edge case:
    100% discount should make price zero
    """
    assert member_price(1000, 100) == 0


def test_member_price_decimal_discount():
    """
    Verify decimal calculations
    """
    assert member_price(999, 10) == 899.1


# -------------------------------------------------
# Tests for add_gst()
# -------------------------------------------------

def test_add_gst_default_rate():
    """
    Default GST rate is 5%
    """
    assert add_gst(1000) == 1050


def test_add_gst_custom_rate():
    """
    Custom GST rate
    """
    assert add_gst(1000, 10) == 1100


def test_add_gst_zero_rate():
    """
    Edge case:
    0% GST should not change price
    """
    assert add_gst(1000, 0) == 1000


# -------------------------------------------------
# Tests for delivery_fee()
# -------------------------------------------------

def test_delivery_fee_below_threshold():
    """
    Orders below 500 should pay delivery fee
    """
    assert delivery_fee(300) == 40


def test_delivery_fee_at_threshold_boundary():
    """
    Edge case:
    Exactly 500 should get free delivery
    """
    assert delivery_fee(500) == 0


def test_delivery_fee_above_threshold():
    """
    Orders above 500 should get free delivery
    """
    assert delivery_fee(600) == 0


def test_delivery_fee_custom_threshold():
    """
    Verify custom free delivery threshold
    """
    assert delivery_fee(1000, free_above=1200, flat=50) == 50


# -------------------------------------------------
# Tests for loyalty_points()
# -------------------------------------------------

def test_loyalty_points_normal_case():
    """
    950 spent gives 9 points
    """
    assert loyalty_points(950) == 9


def test_loyalty_points_exact_hundred():
    """
    Exact multiples of 100
    """
    assert loyalty_points(1000) == 10


def test_loyalty_points_below_hundred():
    """
    Less than 100 gives zero points
    """
    assert loyalty_points(99) == 0


def test_loyalty_points_zero_amount():
    """
    Edge case:
    Zero spending
    """
    assert loyalty_points(0) == 0


    """
    Sample Output:
API_Ingestion/test_pricing.py::test_member_price_decimal_discount PASSED                                                                [ 26%]
API_Ingestion/test_pricing.py::test_add_gst_default_rate PASSED                                                                         [ 33%]
API_Ingestion/test_pricing.py::test_add_gst_custom_rate PASSED                                                                          [ 40%]
API_Ingestion/test_pricing.py::test_add_gst_zero_rate PASSED                                                                            [ 46%]
API_Ingestion/test_pricing.py::test_delivery_fee_below_threshold PASSED                                                                 [ 53%]
API_Ingestion/test_pricing.py::test_delivery_fee_at_threshold_boundary PASSED                                                           [ 60%]
API_Ingestion/test_pricing.py::test_delivery_fee_above_threshold PASSED                                                                 [ 66%]
API_Ingestion/test_pricing.py::test_delivery_fee_custom_threshold PASSED                                                                [ 73%]
API_Ingestion/test_pricing.py::test_loyalty_points_normal_case PASSED                                                                   [ 80%]
API_Ingestion/test_pricing.py::test_loyalty_points_exact_hundred PASSED                                                                 [ 86%]
API_Ingestion/test_pricing.py::test_loyalty_points_below_hundred PASSED                                                                 [ 93%]
API_Ingestion/test_pricing.py::test_loyalty_points_zero_amount PASSED    
    """