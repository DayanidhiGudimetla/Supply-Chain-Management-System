from db import connect
from models import view_products
from validators import validate_positive_int
from utils import print_table, export_to_csv

# ──────────────────────────────────────────────
# ORDER OPERATIONS
# ──────────────────────────────────────────────

def place_order():
    conn = connect()
    cur = conn.cursor()
    try:
        view_products()
        pid = int(input("\n  Product ID: "))
        qty = validate_positive_int(input("  Quantity: "), "Quantity")

        cur.execute("""
            SELECT p.id, p.name, p.stock, p.price, s.status
            FROM products p
            JOIN suppliers s ON s.id = p.supplier_id
            WHERE p.id = ?
        """, (pid,))
        product = cur.fetchone()

        if not product:
            print("  ❌ Product not found.")
            return

        if product["status"] == "inactive":
            print("  ❌ Supplier is inactive. Cannot place order.")
            return

        if qty > product["stock"]:
            print(f"  ❌ Insufficient stock. Available: {product['stock']}")
            return

        total = product["price"] * qty

        print(f"\n  Product : {product['name']}")
        print(f"  Quantity: {qty}")
        print(f"  Total   : ₹{total:.2f}")
        confirm = input("\n  Confirm order? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("  ❌ Order cancelled.")
            return

        # Atomic transaction
        cur.execute("BEGIN")
        cur.execute(
            "INSERT INTO orders (product_id, quantity, total, status) VALUES (?, ?, ?, 'confirmed')",
            (pid, qty, total)
        )
        cur.execute(
            "UPDATE products SET stock = stock - ? WHERE id=?",
            (qty, pid)
        )
        cur.execute(
            "INSERT INTO inventory_logs (product_id, change_qty, reason) VALUES (?, ?, ?)",
            (pid, -qty, f"Order placed - qty {qty}")
        )
        conn.commit()
        print(f"  ✅ Order placed! Total: ₹{total:.2f}")

        # Low stock warning
        cur.execute("SELECT stock, restock_threshold FROM products WHERE id=?", (pid,))
        row = cur.fetchone()
        if row and row["stock"] <= row["restock_threshold"]:
            print(f"  ⚠️  Warning: Stock for this product is now low ({row['stock']} units remaining)!")

    except Exception as e:
        conn.rollback()
        print(f"  ❌ Error: {e}")
    finally:
        conn.close()


def restock_product():
    conn = connect()
    cur = conn.cursor()
    try:
        view_products()
        pid = int(input("\n  Product ID to restock: "))
        qty = validate_positive_int(input("  Restock Quantity: "), "Quantity")

        cur.execute("SELECT id, name FROM products WHERE id=?", (pid,))
        product = cur.fetchone()
        if not product:
            print("  ❌ Product not found.")
            return

        cur.execute("BEGIN")
        cur.execute("UPDATE products SET stock = stock + ? WHERE id=?", (qty, pid))
        cur.execute(
            "INSERT INTO inventory_logs (product_id, change_qty, reason) VALUES (?, ?, ?)",
            (pid, qty, f"Restock - qty {qty}")
        )
        conn.commit()
        print(f"  ✅ '{product['name']}' restocked by {qty} units!")

    except Exception as e:
        conn.rollback()
        print(f"  ❌ Error: {e}")
    finally:
        conn.close()


def view_orders():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT o.id, p.name, o.quantity, o.total, o.status, o.created_at
        FROM orders o
        JOIN products p ON p.id = o.product_id
        ORDER BY o.created_at DESC
    """)
    rows = cur.fetchall()
    conn.close()
    print("\n  --- All Orders ---")
    print_table(["Order ID", "Product", "Quantity", "Total (₹)", "Status", "Date"],
                [tuple(r) for r in rows])


def cancel_order():
    conn = connect()
    cur = conn.cursor()
    try:
        view_orders()
        oid = int(input("\n  Enter Order ID to cancel: "))

        cur.execute("SELECT id, product_id, quantity, status FROM orders WHERE id=?", (oid,))
        order = cur.fetchone()

        if not order:
            print("  ❌ Order not found.")
            return

        if order["status"] == "cancelled":
            print("  ❌ Order is already cancelled.")
            return

        if order["status"] == "delivered":
            print("  ❌ Cannot cancel a delivered order.")
            return

        # Restore stock atomically
        cur.execute("BEGIN")
        cur.execute("UPDATE orders SET status='cancelled' WHERE id=?", (oid,))
        cur.execute("UPDATE products SET stock = stock + ? WHERE id=?",
                    (order["quantity"], order["product_id"]))
        cur.execute(
            "INSERT INTO inventory_logs (product_id, change_qty, reason) VALUES (?, ?, ?)",
            (order["product_id"], order["quantity"], f"Order #{oid} cancelled - stock restored")
        )
        conn.commit()
        print(f"  ✅ Order #{oid} cancelled and stock restored!")

    except Exception as e:
        conn.rollback()
        print(f"  ❌ Error: {e}")
    finally:
        conn.close()


def update_order_status():
    conn = connect()
    cur = conn.cursor()
    try:
        view_orders()
        oid = int(input("\n  Enter Order ID to update: "))

        cur.execute("SELECT id, status FROM orders WHERE id=?", (oid,))
        order = cur.fetchone()
        if not order:
            print("  ❌ Order not found.")
            return

        if order["status"] in ("cancelled", "delivered"):
            print(f"  ❌ Cannot update a '{order['status']}' order.")
            return

        print("  1. pending   2. confirmed   3. shipped   4. delivered")
        choice = input("  Select new status: ").strip()
        status_map = {"1": "pending", "2": "confirmed", "3": "shipped", "4": "delivered"}
        if choice not in status_map:
            print("  ❌ Invalid choice.")
            return

        cur.execute("UPDATE orders SET status=? WHERE id=?", (status_map[choice], oid))
        conn.commit()
        print(f"  ✅ Order #{oid} status updated to '{status_map[choice]}'!")

    except Exception as e:
        print(f"  ❌ Error: {e}")
    finally:
        conn.close()


# ──────────────────────────────────────────────
# ANALYTICS
# ──────────────────────────────────────────────

def analytics():
    conn = connect()
    cur = conn.cursor()

    print("\n  --- Supply Chain Analytics Dashboard ---")

    # Summary
    cur.execute("SELECT COUNT(*) FROM suppliers WHERE status='active'")
    active_suppliers = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM products")
    total_products = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM orders WHERE status != 'cancelled'")
    total_orders = cur.fetchone()[0]

    print(f"\n  🏭 Active Suppliers : {active_suppliers}")
    print(f"  📦 Total Products   : {total_products}")
    print(f"  🛒 Total Orders     : {total_orders}")

    # Revenue
    cur.execute("SELECT SUM(total) FROM orders WHERE status != 'cancelled'")
    revenue = cur.fetchone()[0] or 0
    print(f"  💰 Total Revenue    : ₹{revenue:.2f}")

    # Top selling products
    cur.execute("""
        SELECT p.name, SUM(o.quantity) AS qty_sold, SUM(o.total) AS revenue
        FROM orders o
        JOIN products p ON p.id = o.product_id
        WHERE o.status != 'cancelled'
        GROUP BY p.name
        ORDER BY qty_sold DESC
        LIMIT 5
    """)
    rows = cur.fetchall()
    print("\n  🏆 Top 5 Best-Selling Products:")
    print_table(["Product", "Qty Sold", "Revenue (₹)"], [tuple(r) for r in rows])

    # Supplier performance
    cur.execute("""
        SELECT s.name, COUNT(o.id) AS total_orders, SUM(o.total) AS revenue
        FROM orders o
        JOIN products p ON p.id = o.product_id
        JOIN suppliers s ON s.id = p.supplier_id
        WHERE o.status != 'cancelled'
        GROUP BY s.name
        ORDER BY revenue DESC
    """)
    rows = cur.fetchall()
    print("\n  📊 Supplier Performance:")
    print_table(["Supplier", "Total Orders", "Revenue (₹)"], [tuple(r) for r in rows])

    # Category wise stock
    cur.execute("""
        SELECT category, COUNT(*) AS products, SUM(stock) AS total_stock
        FROM products
        GROUP BY category
        ORDER BY total_stock DESC
    """)
    rows = cur.fetchall()
    print("\n  🗂️  Stock by Category:")
    print_table(["Category", "Products", "Total Stock"], [tuple(r) for r in rows])

    conn.close()


def export_reports():
    conn = connect()
    cur = conn.cursor()

    # Inventory report
    cur.execute("""
        SELECT p.name, p.price, p.stock, p.category, p.restock_threshold, s.name
        FROM products p
        JOIN suppliers s ON s.id = p.supplier_id
    """)
    rows = cur.fetchall()
    export_to_csv("inventory_report.csv",
                  ["Product", "Price (₹)", "Stock", "Category", "Min Threshold", "Supplier"],
                  [tuple(r) for r in rows])

    # Orders report
    cur.execute("""
        SELECT o.id, p.name, o.quantity, o.total, o.status, o.created_at
        FROM orders o
        JOIN products p ON p.id = o.product_id
        ORDER BY o.created_at DESC
    """)
    rows = cur.fetchall()
    export_to_csv("orders_report.csv",
                  ["Order ID", "Product", "Quantity", "Total (₹)", "Status", "Date"],
                  [tuple(r) for r in rows])

    conn.close()
