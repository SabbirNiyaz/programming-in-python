# 💰 Expense Tracker APP — Python Midterm Project

**Track:** Desktop Application (GUI)  
**Library:** tkinter (Python standard library)  
**Storage:** JSON  

---

## 📁 Project Structure

```
expense_tracker_project/
│
├── main.py               # Entry point — run this file
├── expense.py            # Entity class (Expense)
├── expense_manager.py    # Service/Manager class (business logic)
├── storage.py            # Storage class (JSON persistence)
├── gui_app.py            # UI Controller class (tkinter GUI)
│
├── data.json             # Sample data file (auto-created on first run)
├── requirements.txt      # Dependencies
└── README.md             # This file
```

---

## ⚙️ Setup & Run Instructions

### 1. Create virtual environment
```bash
python -m venv .venv
```

### 2. Activate virtual environment
**Windows:**
```bash
.venv\Scripts\activate
```
**macOS / Linux:**
```bash
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python main.py
```

### 5. Freeze requirements (after installing any new packages)
```bash
pip freeze > requirements.txt
```

---

## Features

### CRUD Operations
-  Add new expense (title, category, amount, date)
-  Edit existing expense (click row -> edit form -> Update)
-  Delete expense (with confirmation dialog)
-  View all expenses in a sortable table

### Search & Filter
-  Search by title or category keyword
-  Filter by category dropdown
-  Show all records

### Sort
- Sort by date, amount, or title
- Toggle ascending / descending

### Summary Report
- Total expenses
- Average expense
- Highest single expense
- Record count
- Full report popup with category breakdown + percentages

### Data Persistence
- Auto-saves to `data.json` on every add/update/delete
- Loads data on startup automatically
- Stable IDs — no ID reuse after deletion

### Input Validation
- Empty field detection
- Numeric amount validation
- Date format validation (YYYY-MM-DD)
- Friendly error messages — no crashes

---

##  OOP Design

| Class | Type | Responsibility |
|---|---|---|
| `Expense` | Entity | Represents one expense record; validates fields |
| `ExpenseManager` | Manager/Service | All business logic (CRUD, search, sort, reports) |
| `JsonStorage` | Storage | Load/save JSON; ID generation |
| `ExpenseApp` | UI Controller | Builds GUI; handles events; connects UI to manager |

**Design patterns used:**
- **Composition:** `ExpenseApp` -> `ExpenseManager` -> `JsonStorage`
- **Class method:** `Expense.from_dict()` for loading from JSON
- **Static method:** `Expense.validate()` for reusable validation

---

##  Categories
Food, Transport, Shopping, Health, Education, Entertainment, Bills, Other
