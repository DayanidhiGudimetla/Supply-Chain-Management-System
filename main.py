from models import (
    add_supplier, view_suppliers, update_supplier_status, supplier_inventory,
    add_product, view_products, low_stock_alert,
    view_inventory_logs
)
from operations import (
    place_order, restock_product, view_orders,
    cancel_order, update_order_status,
    analytics, export_reports
)

# ──────────────────────────────────────────────
# MENUS
# ──────────────────────────────────────────────

def main_menu():
    print("\n╔══════════════════════════════════════╗")
    print("║  🚚  Supply Chain Management System  ║")
    print("╚══════════════════════════════════════╝")
    print("  1. 🏭 Supplier Management")
    print("  2. 📦 Product & Inventory")
    print("  3. 🛒 Order Management")
    print("  4. 📊 Analytics Dashboard")
    print("  5. 📁 Export Reports (CSV)")
    print("  6. ❌ Exit")

def supplier_menu():
    print("\n  --- Supplier Management ---")
    print("  1. Add Supplier")
    print("  2. View All Suppliers")
    print("  3. Update Supplier Status")
    print("  4. View Supplier Inventory")
    print("  5. Back")

def product_menu():
    print("\n  --- Product & Inventory ---")
    print("  1. Add Product")
    print("  2. View All Products")
    print("  3. Low Stock Alert")
    print("  4. View Inventory Logs")
    print("  5. Back")

def order_menu():
    print("\n  --- Order Management ---")
    print("  1. Place Order")
    print("  2. Restock Product")
    print("  3. View All Orders")
    print("  4. Update Order Status")
    print("  5. Cancel Order")
    print("  6. Back")

# ──────────────────────────────────────────────
# HANDLERS
# ──────────────────────────────────────────────

def handle_suppliers():
    while True:
        supplier_menu()
        choice = input("\n  Choice: ").strip()
        if choice == "1":   add_supplier()
        elif choice == "2": view_suppliers()
        elif choice == "3": update_supplier_status()
        elif choice == "4": supplier_inventory()
        elif choice == "5": break
        else: print("  ❌ Invalid choice.")

def handle_products():
    while True:
        product_menu()
        choice = input("\n  Choice: ").strip()
        if choice == "1":   add_product()
        elif choice == "2": view_products()
        elif choice == "3": low_stock_alert()
        elif choice == "4": view_inventory_logs()
        elif choice == "5": break
        else: print("  ❌ Invalid choice.")

def handle_orders():
    while True:
        order_menu()
        choice = input("\n  Choice: ").strip()
        if choice == "1":   place_order()
        elif choice == "2": restock_product()
        elif choice == "3": view_orders()
        elif choice == "4": update_order_status()
        elif choice == "5": cancel_order()
        elif choice == "6": break
        else: print("  ❌ Invalid choice.")

# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────

def run():
    while True:
        main_menu()
        choice = input("\n  Choice: ").strip()

        if choice == "1":   handle_suppliers()
        elif choice == "2": handle_products()
        elif choice == "3": handle_orders()
        elif choice == "4": analytics()
        elif choice == "5": export_reports()
        elif choice == "6":
            print("\n  👋 Goodbye!")
            break
        else:
            print("  ❌ Invalid choice.")

if __name__ == "__main__":
    run()
