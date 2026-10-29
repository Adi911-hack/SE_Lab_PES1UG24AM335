
import pytest
from coupon_validator import coupon_discount, best_discount, is_expired


def test_welcome_new_user():
    assert coupon_discount("WELCOME10", 200, True, "mon") == 20


def test_welcome_existing_user():
    assert coupon_discount("WELCOME10", 200, False, "mon") == 0


def test_weekend_large_cart():
    assert coupon_discount("WEEKEND20", 500, False, "sat") == 100


def test_weekend_small_cart():
    assert coupon_discount("WEEKEND20", 200, False, "sun") == 50


def test_weekday_coupon():
    assert coupon_discount("WEEKEND20", 500, False, "mon") == 0


def test_flat_coupon():
    assert coupon_discount("FLAT100", 400, False, "wed") == 100


def test_flat_coupon_below_threshold():
    assert coupon_discount("FLAT100", 300, False, "wed") == 0


def test_unknown_coupon():
    assert coupon_discount("INVALID", 200, True, "mon") == 0


def test_empty_cart():
    with pytest.raises(ValueError):
        coupon_discount("WELCOME10", 0, True, "mon")


def test_best_discount():
    assert best_discount(["WELCOME10", "FLAT100"], 400, True, "mon") == 100


def test_discount_cap():
    assert best_discount(["WEEKEND20"], 100, False, "sun") == 40


def test_expired_coupon():
    assert is_expired(10, 5, 3) is True


def test_valid_coupon():
    assert is_expired(10, 5, 5) is False


def test_invalid_validity():
    assert is_expired(10, 5, 0) is True
