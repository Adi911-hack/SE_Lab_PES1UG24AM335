"""Lab 7 - Aditya Umashankar, PES1UG24AM335.

Invalid input returns None; valid input retains the starter's return types.
expiry_days counts elapsed calendar days from 2024-01-01 (day zero).
"""

from datetime import date
import math
import re

MAX_INPUT_LENGTH = 4096
BASE_DATE = date(2024, 1, 1)


def _text(value):
    if not isinstance(value, str) or len(value) > MAX_INPUT_LENGTH:
        return None
    return value.strip()


def split_code(code):
    """Parse ASCII letters, one hyphen, and a nonnegative integer value."""
    text = _text(code)
    if text is None or re.fullmatch(r"[A-Za-z]+-[0-9]+", text) is None:
        return None
    # Bound the integer conversion independently of Python's digit limit.
    prefix, value = text.split("-")
    if len(value) > 100:
        return None
    return prefix.upper(), int(value)


def most_expensive(prices_csv):
    """Return the maximum finite, nonnegative CSV price; reject empty fields."""
    text = _text(prices_csv)
    if not text:
        return None
    prices = []
    for token in text.split(","):
        token = token.strip()
        if re.fullmatch(r"[+]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?", token) is None:
            return None
        price = float(token)
        if not math.isfinite(price) or price < 0:
            return None
        prices.append(price)
    return max(prices)


def expiry_days(date_text):
    """Return signed elapsed days from 2024-01-01 using the Gregorian calendar."""
    text = _text(date_text)
    if text is None or re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", text) is None:
        return None
    try:
        expiry = date.fromisoformat(text)
    except ValueError:
        return None
    return (expiry - BASE_DATE).days


def main():
    prompts = [
        ("split_code", "Enter a coupon code (e.g. save-20): ", split_code, "Prefix and Value:"),
        ("most_expensive", "Enter item prices as CSV (e.g. 199,49.5,320): ", most_expensive, "Most Expensive Item:"),
        ("expiry_days", "Enter an expiry date as YYYY-MM-DD: ", expiry_days, "Days Since 2024-01-01:"),
    ]
    for name, prompt, function, label in prompts:
        print("==== Running", name, "====")
        try:
            result = function(input(prompt))
        except (EOFError, KeyboardInterrupt):
            print("\nInput cancelled.")
            return
        print(label, result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()
