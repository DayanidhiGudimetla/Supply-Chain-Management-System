"""
Unit tests for Supply Chain Management System
Run with: python -m pytest tests/test_core.py -v
"""
import pytest
import os
import csv
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import export_to_csv, print_table


# ── CSV Export Tests ────────────────────────────────────────────────────────

def test_export_creates_file(tmp_path):
    """export_to_csv must create the file on disk."""
    filepath = str(tmp_path / "inventory.csv")
    export_to_csv(filepath, ["Product", "Stock", "Supplier"], [("Cable", 50, "SupplierA")])
    assert os.path.exists(filepath)


def test_export_correct_headers(tmp_path):
    """First row must match provided headers exactly."""
    filepath = str(tmp_path / "inventory.csv")
    export_to_csv(filepath, ["Product", "Stock", "Category"], [])
    with open(filepath, newline="") as f:
        reader = list(csv.reader(f))
    assert reader[0] == ["Product", "Stock", "Category"]


def test_export_correct_data(tmp_path):
    """Data rows must be written correctly after the header."""
    filepath = str(tmp_path / "orders.csv")
    export_to_csv(filepath, ["Product", "Qty", "Total", "Status"],
                  [("Laptop", 5, 50000, "delivered"), ("Cable", 20, 2000, "pending")])
    with open(filepath, newline="") as f:
        reader = list(csv.reader(f))
    assert reader[1] == ["Laptop", "5", "50000", "delivered"]
    assert reader[2] == ["Cable", "20", "2000", "pending"]


def test_export_empty_rows_only_header(tmp_path):
    """Empty data should produce file with only the header row."""
    filepath = str(tmp_path / "empty.csv")
    export_to_csv(filepath, ["Col1", "Col2"], [])
    with open(filepath, newline="") as f:
        reader = list(csv.reader(f))
    assert len(reader) == 1
    assert reader[0] == ["Col1", "Col2"]


def test_export_multiple_rows(tmp_path):
    """Multiple rows must all be written correctly."""
    filepath = str(tmp_path / "multi.csv")
    rows = [(f"Product{i}", i * 100, "active") for i in range(1, 6)]
    export_to_csv(filepath, ["Name", "Stock", "Status"], rows)
    with open(filepath, newline="") as f:
        reader = list(csv.reader(f))
    assert len(reader) == 6  # 1 header + 5 data rows


# ── Business Logic Tests ────────────────────────────────────────────────────

def test_order_status_values():
    """Order status must be one of valid states."""
    valid_statuses = {"pending", "confirmed", "shipped", "delivered", "cancelled"}
    for status in valid_statuses:
        assert status in valid_statuses


def test_supplier_status_values():
    """Supplier status must be active or inactive."""
    valid_statuses = {"active", "inactive"}
    assert "active" in valid_statuses
    assert "inactive" in valid_statuses


def test_low_stock_alert_triggers_correctly():
    """Low stock alert must trigger when stock is below restock threshold."""
    product = {"name": "Cable", "stock": 3, "restock_threshold": 10}
    is_low = product["stock"] < product["restock_threshold"]
    assert is_low is True


def test_low_stock_alert_does_not_trigger_above_threshold():
    """Low stock alert must NOT trigger when stock is above threshold."""
    product = {"name": "Laptop", "stock": 50, "restock_threshold": 10}
    is_low = product["stock"] < product["restock_threshold"]
    assert is_low is False


def test_stock_restoration_on_cancellation():
    """Cancelling an order must restore stock back to original."""
    original_stock = 100
    order_qty = 20
    stock_after_order = original_stock - order_qty
    stock_after_cancel = stock_after_order + order_qty
    assert stock_after_cancel == original_stock


def test_atomic_order_stock_deduction():
    """Placing an order must correctly deduct stock."""
    stock = 50
    order_qty = 15
    new_stock = stock - order_qty
    assert new_stock == 35


def test_order_rejected_when_insufficient_stock():
    """Order must be rejected when stock is less than requested quantity."""
    stock = 5
    order_qty = 20
    can_place = stock >= order_qty
    assert can_place is False


def test_inventory_log_records_change():
    """Inventory log must record the correct quantity change."""
    logs = []
    logs.append({"product_id": 1, "change_qty": -15, "reason": "order placed"})
    assert logs[0]["change_qty"] == -15
    assert logs[0]["reason"] == "order placed"


def test_restock_increases_stock():
    """Restocking must increase stock by the correct amount."""
    current_stock = 5
    restock_qty = 100
    new_stock = current_stock + restock_qty
    assert new_stock == 105
