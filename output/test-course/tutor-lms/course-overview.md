# Validate and Clean CSV Data with Python

## Audience
Beginners who know basic Python syntax (variables, functions, loops) but have no prior data engineering experience.

## Level
Beginner

## Prerequisites
Basic Python (variables, functions, for loops). No pandas experience required.

## Estimated duration
1 hour total — approximately 20 minutes of lessons and 40 minutes of hands-on lab work (~66% practical).

## Technologies
Python 3.11+, pandas, pytest, CSV

## Business scenario
A small online bookstore receives a daily CSV export of book orders from its e-commerce platform. The export regularly contains rows with a missing unit price, a zero or negative quantity, and duplicated order IDs caused by webhook retries. The reporting team cannot trust the numbers until the file is validated and cleaned.

## Deliverable
A `clean_orders.py` script that reads `orders.csv`, produces `clean_orders.csv` and `quarantine_orders.csv`, and passes the provided pytest suite.

## Validation criteria
Running `pytest` against `tests/test_clean_orders.py` exits with status 0:
- `clean_orders.csv` contains exactly the valid, deduplicated rows (first occurrence kept per `order_id`).
- `quarantine_orders.csv` contains exactly the rows with a missing/invalid unit price or a non-positive quantity.

## Acquired skills
- Explaining why data must be validated before it is trusted for reporting.
- Building pandas boolean masks to detect invalid records.
- Separating valid data from invalid data instead of silently dropping or crashing on it.
- Deduplicating records deterministically by a business key.
- Verifying a small data pipeline with automated tests.

## Curriculum structure
1 topic, 3 lessons, 2 quizzes, 1 practical lab. See `curriculum.md` for the full breakdown.
