# 🚚 Supply Chain Management System

A fully functional **Supply Chain Management CLI application** built with **Python and SQLite** — featuring supplier management, product inventory tracking, order processing, restock workflow, analytics dashboard, and CSV report export.

---

## 📌 Features

### 🏭 Supplier Management
- Add suppliers with contact and email
- View all suppliers with status
- Activate / deactivate suppliers
- View all products per supplier

### 📦 Product & Inventory
- Add products with price, stock, category, restock threshold
- View full product inventory with supplier info
- Low stock alerts based on configurable threshold per product
- Full inventory log history (every stock change tracked)

### 🛒 Order Management
- Place orders with real-time stock validation
- Atomic transactions — rolls back on failure
- Auto low stock warning after order placement
- Restock products with inventory log entry
- Update order status (pending → confirmed → shipped → delivered)
- Cancel orders with automatic stock restoration

### 📊 Analytics Dashboard
- Total active suppliers, products, orders, revenue
- Top 5 best-selling products
- Supplier-wise performance (orders + revenue)
- Category-wise stock summary

### 📁 Export Reports
- `inventory_report.csv` — full product inventory
- `orders_report.csv` — complete order history

---

## 🗂️ Project Structure

```
supply_chain_project/
│── main.py          # CLI entry point & menus
│── db.py            # Database connection
│── models.py        # Supplier, Product, Inventory operations
│── operations.py    # Orders, Analytics, Export
│── validators.py    # Input validation functions
│── utils.py         # Table printer, CSV export
│── schema.sql       # Database schema
│── init_db.py       # Database initializer
│── README.md
```

---

## 🗄️ Database Schema

```
suppliers       → id, name, contact, email, status, created_at
products        → id, name, stock, price, category, restock_threshold, supplier_id, created_at
orders          → id, product_id, quantity, total, status, created_at
inventory_logs  → id, product_id, change_qty, reason, logged_at
```

---

## ⚙️ Tech Stack

- **Language:** Python 3
- **Database:** SQLite3
- **Data Export:** CSV

---

## 🚀 How to Run

### 1. Initialize the database
```bash
python init_db.py
```

### 2. Run the application
```bash
python main.py
```

---

## 📋 Workflow

```
Add Supplier → Add Product → Place Order → Update Status → Delivered
                    ↓
              Low Stock Alert → Restock Product → Inventory Log Updated
```

---

## 👨‍💻 Author

**Dayanidhi Gudimetla**
GitHub: [github.com/DayanidhiGudimetla](https://github.com/DayanidhiGudimetla)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
