# Expense Tracker APP — Python Midterm Project  

**Track:** Desktop Application (GUI)  
**Library:** tkinter (Python standard library)  
**Storage:** JSON  

---

## Project Structure

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

## Setup & Run Instructions

### Option 1: Run from GitHub (Recommended)

1. Clone the repository (sparse checkout for efficiency)
```bash
git clone --filter=blob:none --sparse https://github.com/SabbirNiyaz/programming-in-python.git
```

2. Navigate into the project
```bash
cd programming-in-python
```

3. Pull only the required project folder
```bash
git sparse-checkout set mid_term_project/expense_tracker_app
```

4. Open the project in VS Code
- Navigate to the `expense_tracker_app` folder  
- Open it with VS Code  

---

### Environment Setup

5. Create a virtual environment
```bash
python -m venv .venv
```

6. Activate the virtual environment

Windows:
```bash
.venv\Scripts\activate
```

macOS / Linux:
```bash
source .venv/bin/activate
```

7. Install dependencies
```bash
pip install -r requirements.txt
```

---

### Run the Application

8. Start the app
```bash
python main.py
```

---

### Freeze Dependencies (Optional)

```bash
pip freeze > requirements.txt
```

---

## Features

### CRUD Operations
- Add new expense (title, category, amount, date)  
- Edit existing expense (click row → edit form → Update)  
- Delete expense (with confirmation dialog)  
- View all expenses in a sortable table  

### Search & Filter
- Search by title or category keyword  
- Filter by category dropdown  
- Show all records  

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
- Stable IDs (no reuse after deletion)  

### Input Validation
- Empty field detection  
- Numeric amount validation  
- Date format validation (YYYY-MM-DD)  
- Friendly error messages (no crashes)  

---

## OOP Design

| Class            | Type            | Responsibility                                     |
|------------------|-----------------|----------------------------------------------------|
| `Expense`        | Entity          | Represents one expense; validates fields           |
| `ExpenseManager` | Manager/Service | Handles CRUD, search, sort, and reports            |
| `JsonStorage`    | Storage         | Manages JSON load/save and ID generation           |
| `ExpenseApp`     | UI Controller   | Builds GUI and connects UI with logic              |

### Design Patterns Used
- Composition: `ExpenseApp → ExpenseManager → JsonStorage`  
- Class Method: `Expense.from_dict()` for JSON loading  
- Static Method: `Expense.validate()` for reusable validation  

---

## Categories

Food, Transport, Shopping, Health, Education, Entertainment, Bills, Other  