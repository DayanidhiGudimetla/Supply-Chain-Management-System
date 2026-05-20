# ⛓️ Supply Chain Management System

A fully functional **Supply Chain Management CLI application** built with **Python and SQLite** — featuring supplier management, product inventory tracking, atomic order processing, configurable restock thresholds, full inventory audit logging, and CSV report export.

---

## 📌 Features

### 🏭 Supplier Management
- Add suppliers with contact and email details
- View all suppliers with status (active / inactive)
- Activate / deactivate suppliers
- View all products per supplier

### 📦 Product & Inventory
- Add products with price, stock, category and **configurable restock threshold per product**
- View full product inventory with supplier info
- Low stock alerts triggered automatically based on per-product threshold
- Full **inventory audit log** — every stock change tracked with reason and timestamp

### 🛒 Order Management
- Place orders with **real-time stock validation**
- **Atomic transactions** — full rollback if anything fails
- Auto low stock warning after order placement
- Restock products with inventory log entry
- Update order status: pending → confirmed → shipped → delivered
- Cancel orders with **automatic stock restoration**

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
│── tests/
│   ├── __init__.py
│   └── test_core.py # 14 pytest unit tests
└── README.md
```

---

## 🗄️ Database Schema

| Table | Description |
| --- | --- |
| `suppliers` | id, name, contact, email, status, created_at |
| `products` | id, name, stock, price, category, restock_threshold, supplier_id, created_at |
| `orders` | id, product_id, quantity, total, status, created_at |
| `inventory_logs` | id, product_id, change_qty, reason, logged_at |

---

## ⚙️ Tech Stack

| Layer | Technology |
| --- | --- |
| Language | Python 3 |
| Database | SQLite3 |
| Data Export | CSV (built-in) |
| Testing | pytest |

---

## 🚀 How to Run

### 1. Clone the repository
```
git clone https://github.com/DayanidhiGudimetla/Supply-Chain-Management-System.git
cd Supply-Chain-Management-System
```

### 2. Initialize the database
```
python init_db.py
```

### 3. Run the application
```
python main.py
```
> No external dependencies required — uses Python standard library only.

---

## 🧪 Running Tests

```
python -m pip install pytest
python -m pytest tests/test_core.py -v
```

### Test Coverage

| Test Area | Cases Covered |
| --- | --- |
| CSV export | File creation, header accuracy, data rows, empty data, multiple rows |
| Order logic | Stock deduction, rejection on insufficient stock, restoration on cancel |
| Inventory log | Change quantity recorded correctly on order and restock |
| Low stock alert | Triggers below threshold, does not trigger above threshold |
| Status validation | Order and supplier status values |

**14 tests — all passing ✅**

---

## 📋 Workflow

```
Add Supplier → Add Product → Place Order → Update Status → Delivered
                    ↓
              Low Stock Alert → Restock Product → Inventory Log Updated
```

---

## 🔒 Business Rules

- Orders are **rejected** if stock is less than requested quantity
- Cancelling an order **automatically restores** stock to original level
- Every stock change (order, restock, cancel) is **logged in inventory_logs** with reason
- Each product has its own **configurable restock threshold** — not a global setting
- Order status transitions: pending → confirmed → shipped → delivered

---

## 📊 Analytics Available

- 💰 Total revenue from all delivered orders
- 🏭 Total active suppliers and products
- 🏆 Top 5 best-selling products by quantity
- 📦 Supplier-wise order count and revenue
- 📂 Category-wise stock summary
- 📄 Export to CSV — inventory and orders reports

---

## 👨‍💻 Author

**Dayanidhi Gudimetla**
- 📧 gudimetladaya11@gmail.com
- 🔗 [LinkedIn](https://www.linkedin.com/in/dayanidhi-gudimetla-2b08013ab)
- 🐙 [GitHub](https://github.com/DayanidhiGudimetla)

---

## 📄 License

This project is open source and available under the [MIT License](https://github.com/DayanidhiGudimetla/Supply-Chain-Management-System/blob/master/LICENSE).
