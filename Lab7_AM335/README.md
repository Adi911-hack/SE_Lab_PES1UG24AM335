# Lab 7: Fuzzing for Input Validation Bugs

**Name:** Aditya Umashankar  
**SRN:** PES1UG24AM335

## Submission

- `Lab7_AM335_Report.pdf`: report with the four required execution screenshots.
- `coupon_validator.py`: fixed application, preserving the assigned function names.
- `test_coupon_validator.py`: completed Hypothesis tests and regression tests.
- `processor.py` / `test_processor.py`: compatibility entry points for the handout's generic commands.
- `original/`: unchanged assigned files for comparison (the original test template is intentionally incomplete).
- `evidence/`: actual terminal screenshots and raw execution logs.
- `reproduce.py`: portable before/after verification; checks expected exit codes.

Source: https://github.com/SETAPESU26/L6_L7_31_coupon_validator/tree/d2005e7d222c58794044b29565b7d1f4439d5498/lab7

## Run

From this folder, after installing Python (3.8+; tested on 3.12):

```sh
python -m pip install -r requirements.txt
python processor.py
python -m pytest test_processor.py -q
```

The repository filenames also work:

```sh
python coupon_validator.py
python -m pytest test_coupon_validator.py -q
```

Run `python reproduce.py` to recreate the before/after logs. The baseline failure is expected and is checked separately from the fixed suite. Plain `python -m pytest -q` collects the canonical suite once; original templates are excluded.

## Validation contract and fixes

Invalid inputs return `None`, which the CLI displays as `Invalid input` and continues. Values must be strings of at most 4096 characters; outer whitespace is ignored.

| Function | Accepted input and result | Fix |
| --- | --- | --- |
| `split_code` | ASCII letters, one hyphen, 1-100 ASCII decimal digits; uppercase prefix and integer tuple | Reject wrong types, missing/extra fields, negative or malformed values and oversized integers |
| `most_expensive` | Nonempty CSV of finite nonnegative decimal prices (optional plus sign/exponent); maximum float | Reject empty fields, nonnumbers, NaN, infinity, overflow and negatives |
| `expiry_days` | Valid zero-padded `YYYY-MM-DD`; signed calendar-day difference from 2024-01-01 | Use real Gregorian dates, including leap years, and reject impossible dates |

The original label says "Days Since 2024"; the fixed version defines the baseline explicitly as 2024-01-01, with that date equal to day zero. Earlier dates return a negative difference. This function is not a calculation from today's date.

## Results

- Original: all three no-crash properties fail (3 failed, 67 deselected); `None` and empty strings expose exceptions. A `bad` coupon crashes the CLI.
- Fixed: **70 passed** with either test filename.
- Six property tests use `max_examples=300`, deterministic generation and no timing deadline. The other tests cover explicit invalid inputs, calendar boundaries, normal examples and the CLI. Generated examples are not counted as separate pytest tests.
- The original returns 61 for 2024-03-01; the correct elapsed difference is 60. 2025-01-01 is 366 days after the baseline.
- Screenshots were captured from real Linux terminal runs. Test environment: Python 3.12, pytest 9.2.0, Hypothesis 6.170.15. External pytest plugins were disabled for the evidence run to isolate this project.

The input-length and coupon-value bounds are defensive design choices, not business rules supplied by the starter. Float prices retain the starter's float representation; this is not an accounting-precision library.
