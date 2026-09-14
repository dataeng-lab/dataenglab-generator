"""Deterministic automated checks for the Validate and Clean CSV Data lab.

Run with: pytest
(from anywhere — paths are resolved relative to this file, not the cwd.)
"""
import sys
from pathlib import Path

import pandas as pd
import pytest

LAB_ROOT = Path(__file__).resolve().parents[1]
STARTER_DIR = LAB_ROOT / "starter"
DATASET_PATH = LAB_ROOT / "datasets" / "orders.csv"

sys.path.insert(0, str(STARTER_DIR))
import clean_orders  # noqa: E402  (import after sys.path setup is intentional)

EXPECTED_QUARANTINE_IDS = {1002, 1003, 1006, 1007}
EXPECTED_CLEAN_IDS = {1001, 1004, 1005, 1008, 1009}


@pytest.fixture
def raw_df():
    return clean_orders.load_orders(DATASET_PATH)


def test_load_orders_reads_all_rows(raw_df):
    assert len(raw_df) == 10


def test_validate_orders_accounts_for_every_row(raw_df):
    valid_df, quarantine_df = clean_orders.validate_orders(raw_df)
    assert len(valid_df) + len(quarantine_df) == len(raw_df)


def test_validate_orders_quarantines_missing_price(raw_df):
    _, quarantine_df = clean_orders.validate_orders(raw_df)
    assert 1002 in set(quarantine_df["order_id"])
    assert 1007 in set(quarantine_df["order_id"])


def test_validate_orders_quarantines_non_positive_quantity(raw_df):
    _, quarantine_df = clean_orders.validate_orders(raw_df)
    assert 1003 in set(quarantine_df["order_id"])
    assert 1006 in set(quarantine_df["order_id"])


def test_validate_orders_exact_quarantine_set(raw_df):
    _, quarantine_df = clean_orders.validate_orders(raw_df)
    assert set(quarantine_df["order_id"]) == EXPECTED_QUARANTINE_IDS


def test_validate_orders_keeps_valid_candidates(raw_df):
    valid_df, _ = clean_orders.validate_orders(raw_df)
    # 1004 appears twice among the valid candidates before dedup.
    assert len(valid_df) == 6
    assert set(valid_df["order_id"]) == EXPECTED_CLEAN_IDS


def test_deduplicate_orders_keeps_first_occurrence_only(raw_df):
    valid_df, _ = clean_orders.validate_orders(raw_df)
    clean_df = clean_orders.deduplicate_orders(valid_df)
    assert len(clean_df) == 5
    assert clean_df["order_id"].is_unique
    assert (clean_df["order_id"] == 1004).sum() == 1


def test_run_pipeline_writes_expected_files(tmp_path):
    clean_df, quarantine_df = clean_orders.run_pipeline(DATASET_PATH, tmp_path)

    assert len(clean_df) == 5
    assert len(quarantine_df) == 4
    assert set(clean_df["order_id"]) == EXPECTED_CLEAN_IDS
    assert set(quarantine_df["order_id"]) == EXPECTED_QUARANTINE_IDS

    clean_path = tmp_path / "clean_orders.csv"
    quarantine_path = tmp_path / "quarantine_orders.csv"
    assert clean_path.is_file()
    assert quarantine_path.is_file()

    written_clean = pd.read_csv(clean_path)
    written_quarantine = pd.read_csv(quarantine_path)
    assert len(written_clean) == 5
    assert len(written_quarantine) == 4
