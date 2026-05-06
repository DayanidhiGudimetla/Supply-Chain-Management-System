from db import connect
from validators import (validate_non_empty, validate_positive_float,
                        validate_non_negative_int, validate_positive_int,
                        validate_phone, validate_email)
from utils import print_table

# ──────────────────────────────────────────────
# SUPPLIER OPERATIONS
# ──────────────────────────────────────────────

def add_supplier():
    conn = connect()
    cur = conn.cursor()
    try:
        name    = validate_non_empty(input("  Supplier Name: "), "Name")
        contact = validate_phone(input("  Contact (10 digits, optional): "))
        email   = validate_email(input("  Email (optional): "))

        cur.execute(
            "INSERT INTO suppliers (name, contact, email) VALUES (?, ?, ?)",
            (name, contact, email)
        )
        conn.commit()
        print("  ✅ Supplier added successfully!")

    except Exception as e:
        print(f"  ❌ Error: {e}")
    finally:
        conn.close()


def view_suppliers():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, name, contact, email, status, created_at FROM suppliers ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    print("\n  --- Suppliers List ---")
    print_table(["ID", "Name", "Contact", "Email", "Status", "Joined At"],
                [tuple(r) for r in rows])


def update_supplier_status():
    conn = connect()
    cur = conn.cursor()
    try:
        view_suppliers()
        sid = int(input("\n  Enter Supplier ID: "))
        cur.execute("SELECT id, name FROM suppliers WHERE id=?", (sid,))
        supplier = cur.fetchone()
        if not supplier:
            print("  ❌ Supplier not found.")
            return

        print("  1. active   2. inactive")
        choice = input("  Select status: ").strip()
        status_map = {"1": "active", "2": "inactive"}
        if choice not in status_map:
            print("  ❌ Invalid choice.")
            return

        cur.execute("UPDATE suppliers SET status=? WHERE id=?", (status_map[choice], sid))
        conn.commit()
        print(f"  ✅ Supplier '{supplier['name']}' status updated to '{status_map[choice]}'!")

    except Exception as e:
        print(f"  ❌ Error: {e}")
    finally:
        conn.close()


# ──────────────────────────────────────────────
# PRODUCT OPERATIONS
# ──────────────────────────────────────────────

def add_product():
    conn = connect()
    cur = conn.cursor()
    try:
        view_suppliers()
        name      = validate_non_empty(input("\n  Product Name: "), "Name")
        price     = validate_positive_float(input("  Price (₹): "), "Price")
        stock     = validate_non_negative_int(input("  Initial Stock: "), "Stock")
        category  = input("  Category (default: General): ").strip() or "General"
        threshold = validate_positive_int(input("  Restock Threshold (default 10): ") or "10", "Threshold")
        sid       = int(input("  Supplier ID: "))

        cur.execute("SELECT id FROM suppliers WHERE id=?", (sid,))
        if not cur.fetchone():
            print("  ❌ Supplier not found.")
            return

        cur.execute(
            "INSERT INTO products (name, price, stock, category, restock_threshold, supplier_id) VALUES (?, ?, ?, ?, ?, ?)",
            (name, price, stock, category, threshold, sid)
        )
        conn.commit()
        print("  ✅ Product added successfully!")

    except Exception as e:
        print(f"  ❌ Error: {e}")
    finally:
        conn.close()


def view_products():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.id, p.name, p.price, p.stock, p.category, p.restock_threshold, s.name AS supplier
        FROM products p
        JOIN suppliers s ON s.id = p.supplier_id
        ORDER BY p.category, p.name
    """)
    rows = cur.fetchall()
    conn.close()
    print("\n  --- Product Inventory ---")
    print_table(["ID", "Name", "Price (₹)", "Stock", "Category", "Min Threshold", "Supplier"],
                [tuple(r) for r in rows])


def low_stock_alert():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.id, p.name, p.stock, p.restock_threshold, s.name AS supplier
        FROM products p
        JOIN suppliers s ON s.id = p.supplier_id
        WHERE p.stock <= p.restock_threshold
        ORDER BY p.stock ASC
    """)
    rows = cur.fetchall()
    conn.close()
    print("\n  --- ⚠️  Low Stock Alert ---")
    print_table(["ID", "Product", "Current Stock", "Min Threshold", "Supplier"],
                [tuple(r) for r in rows])


def view_inventory_logs():
    conn = connect()
    cur = conn.cursor()
    try:
        view_products()
        pid = int(input("\n  Enter Product ID to view logs (0 for all): "))

        if pid == 0:
            cur.execute("""
                SELECT il.id, p.name, il.change_qty, il.reason, il.logged_at
                FROM inventory_logs il
                JOIN products p ON p.id = il.product_id
                ORDER BY il.logged_at DESC
            """)
        else:
            cur.execute("""
                SELECT il.id, p.name, il.change_qty, il.reason, il.logged_at
                FROM inventory_logs il
                JOIN products p ON p.id = il.product_id
                WHERE il.product_id = ?
                ORDER BY il.logged_at DESC
            """, (pid,))

        rows = cur.fetchall()
        print("\n  --- Inventory Log History ---")
        print_table(["Log ID", "Product", "Change", "Reason", "Logged At"],
                    [tuple(r) for r in rows])

    except Exception as e:
        print(f"  ❌ Error: {e}")
    finally:
        conn.close()


def supplier_inventory():
    conn = connect()
    cur = conn.cursor()
    try:
        view_suppliers()
        sid = int(input("\n  Enter Supplier ID: "))

        cur.execute("SELECT name FROM suppliers WHERE id=?", (sid,))
        supplier = cur.fetchone()
        if not supplier:
            print("  ❌ Supplier not found.")
            return

        cur.execute("""
            SELECT id, name, price, stock, category, restock_threshold
            FROM products WHERE supplier_id=?
            ORDER BY name
        """, (sid,))
        rows = cur.fetchall()
        print(f"\n  --- Products from '{supplier['name']}' ---")
        print_table(["ID", "Product", "Price (₹)", "Stock", "Category", "Min Threshold"],
                    [tuple(r) for r in rows])

    except Exception as e:
        print(f"  ❌ Error: {e}")
    finally:
        conn.close()
