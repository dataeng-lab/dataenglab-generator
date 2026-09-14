# Course Request

## Title
Validate and Clean CSV Data with Python

## Slug
test-course

## Audience
Beginners who know basic Python syntax (variables, functions, loops) but have no prior data engineering experience.

## Level
Beginner

## Duration
1 hour

## Technologies
Python 3.11+, pandas, pytest, CSV

## Prerequisites
Basic Python (variables, functions, for loops). No pandas experience required.

## Scenario
A small online bookstore receives a daily CSV export of book orders from its e-commerce platform. The export regularly contains rows with a missing unit price, a zero or negative quantity, and duplicated order IDs caused by webhook retries. The reporting team cannot trust the numbers until the file is validated and cleaned.

## Tasks
Load the raw orders CSV, validate required fields, quarantine rows with a missing/invalid price or a non-positive quantity, deduplicate remaining rows by order ID (keep first occurrence), write a clean orders CSV and a quarantine CSV, and pass all automated tests.

## Outcomes
Students must be able to explain why data validation matters before reporting, build pandas boolean masks to detect invalid rows, separate valid data from invalid data instead of silently dropping or crashing on it, deduplicate records deterministically, and verify a data pipeline with automated tests.

## Deliverable
A `clean_orders.py` script that reads `orders.csv`, produces `clean_orders.csv` and `quarantine_orders.csv`, and passes the provided pytest suite.

## Validation criteria
`pytest` run against `tests/test_clean_orders.py` exits with status 0. Clean output contains exactly the valid, deduplicated rows. Quarantine output contains exactly the invalid rows.

## Note
This is a small end-to-end test course used to validate the DataEngLab course factory pipeline (curriculum, lessons, quizzes, lab, tests, instructor materials, checks, packaging) rather than a full-length flagship course.
