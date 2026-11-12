"""Property-based fuzzing and regression tests for all three assigned functions."""
from datetime import date
import math
import pytest
from hypothesis import example, given, settings, strategies as st
from coupon_validator import split_code, most_expensive, expiry_days

settings.register_profile("lab7", max_examples=300, derandomize=True, deadline=None)
settings.load_profile("lab7")

unexpected = st.one_of(st.none(), st.text(), st.integers(), st.floats(),
                       st.booleans(), st.binary(), st.lists(st.integers()),
                       st.dictionaries(st.text(max_size=5), st.integers()))


@given(unexpected)
@example(None)
@example("")
def test_split_code_no_crash(value):
    result = split_code(value)
    assert result is None or (isinstance(result, tuple) and len(result) == 2
                              and isinstance(result[0], str) and isinstance(result[1], int))


@given(unexpected)
@example(None)
@example("")
def test_most_expensive_no_crash(value):
    result = most_expensive(value)
    assert result is None or (isinstance(result, float) and math.isfinite(result) and result >= 0)


@given(unexpected)
@example(None)
@example("")
def test_expiry_days_no_crash(value):
    result = expiry_days(value)
    assert result is None or isinstance(result, int)


@given(st.text(alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=1, max_size=30),
       st.integers(min_value=0, max_value=10**30))
def test_valid_coupon_round_trip(prefix, value):
    assert split_code("  " + prefix + "-" + str(value) + "  ") == (prefix.upper(), value)


@given(st.lists(st.integers(min_value=0, max_value=10**9), min_size=1, max_size=30))
def test_valid_price_maximum(prices):
    csv = ", ".join(str(price) for price in prices)
    assert most_expensive(csv) == float(max(prices))
    assert most_expensive(",".join(str(price) for price in reversed(prices))) == float(max(prices))


@given(st.dates())
def test_calendar_difference(expiry):
    assert expiry_days(expiry.isoformat()) == (expiry - date(2024, 1, 1)).days


@pytest.mark.parametrize("value", [None, "", "save", "-20", "save-", "save--1", "save-1-2",
    "save-1.5", "save-NaN", "s ave-20", "123-20", "save-١", "ß-20", "save-" + "9"*101,
    "x"*4097, 23, [], {}])
def test_invalid_coupon(value):
    assert split_code(value) is None


@pytest.mark.parametrize("value", [None, "", " ", ",", "1,,2", "1,", ",1", "x,2", "nan", "NaN,2",
    "inf", "-inf", "1e309", "-1,2", "1_000", "١٢", "x"*4097, 23, [], {}])
def test_invalid_prices(value):
    assert most_expensive(value) is None


@pytest.mark.parametrize("value", [None, "", "2024", "2024-1-01", "0000-01-01", "2024-13-01",
    "2024-00-01", "2024-01-00", "2024-04-31", "2023-02-29", "2024-02-30", "2024-01-01-extra",
    "２０２４-01-01", "x"*4097, 23, [], {}])
def test_invalid_dates(value):
    assert expiry_days(value) is None


@pytest.mark.parametrize("text,expected", [("2024-01-01", 0), ("2024-02-29", 59),
    ("2024-03-01", 60), ("2025-01-01", 366), ("2023-12-31", -1)])
def test_calendar_regressions(text, expected):
    assert expiry_days(text) == expected


def test_normal_examples():
    assert split_code("save-20") == ("SAVE", 20)
    assert split_code("SAVE-0") == ("SAVE", 0)
    assert most_expensive("199,49.5,320") == 320.0
    assert most_expensive("0,.5,1e2") == 100.0


@pytest.mark.parametrize("module_name", ["coupon_validator", "processor"])
def test_cli_invalid_input_continues(monkeypatch, capsys, module_name):
    import importlib
    answers = iter(["bad", "nan", "2024-02-30"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))
    importlib.import_module(module_name).main()
    assert capsys.readouterr().out.count("Invalid input") == 3


def test_cli_eof_is_handled(monkeypatch, capsys):
    def eof(prompt):
        raise EOFError
    monkeypatch.setattr("builtins.input", eof)
    from coupon_validator import main
    main()
    assert "Input cancelled" in capsys.readouterr().out
