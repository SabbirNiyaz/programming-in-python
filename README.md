# Programming in Python — Course Projects

**Student:** Sabbir Hossain Niyaz &nbsp;|&nbsp; **ID:** 22-47538-2 &nbsp;|&nbsp; **Course:** Programming in Python

---

## 📁 Projects Overview

| # | Project | Type | Tools / Stack |
|---|---------|------|---------------|
| 1 | [Expense Tracker Desktop App](#-mid-term-project--expense-tracker-desktop-app) | Mid-Term | Python, tkinter, JSON |
| 2 | [Dhaka Rental Housing Market Analysis](#-final-project--analysis-of-the-rental-housing-market-in-dhaka) | Final | Python, Pandas, NumPy, Matplotlib |

---

## 💰 Mid-Term Project — Expense Tracker Desktop Application

A fully functional **personal expense tracker** desktop app built with Python and tkinter. Designed to demonstrate core Python concepts, OOP principles, and real-world application development.

### Features

- ✅ **CRUD Operations** — Add, view, edit, and delete expense records
- 🔍 **Search & Filter** — Case-insensitive search by title or category; filter by category dropdown
- 🔃 **Sort** — Sort records by date, amount, or title (ascending/descending)
- 📊 **Live Summary Report** — Auto-updating total, average, highest expense, and record count
- 💾 **Data Persistence** — All data stored in `data.json`; survives app restarts
- 🛡️ **Input Validation** — Enforces non-empty titles, numeric amounts > 0, and `YYYY-MM-DD` date format

### Project Structure

```
expense_tracker_project/
├── main.py               # Entry point
├── expense.py            # Expense entity class
├── expense_manager.py    # Business logic
├── storage.py            # JSON file handling
├── gui_app.py            # GUI controller
├── data.json             # Persisted expense data
├── requirements.txt      # Dependencies
└── README.md             # Setup instructions
```

### OOP Design

| Class | File | Responsibility |
|-------|------|----------------|
| `Expense` | `expense.py` | Entity: attributes, `to_dict()`, `from_dict()`, `validate()` |
| `JsonStorage` | `storage.py` | File I/O: `save()`, `load()`, `get_next_id()` |
| `ExpenseManager` | `expense_manager.py` | Logic: add, update, delete, search, filter, sort, report |
| `ExpenseApp` | `gui_app.py` | UI controller: layout, button actions, table refresh |

> **OOP concepts used:** Classes & constructors, Composition (`App → Manager → Storage`), Encapsulation, Class/static methods

### Setup & Run

```bash
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

### Data Format (`data.json`)

```json
[
  {
    "id": 1,
    "title": "Lunch",
    "category": "Food",
    "amount": 350.0,
    "date": "2026-03-27"
  }
]
```

---

## 🏠 Final Project — Analysis of the Rental Housing Market in Dhaka

A data analysis project investigating Dhaka's residential rental market using a real-world dataset from Kaggle (scraped from [bproperty.com](https://www.bproperty.com)).

**Instructor:** Md. Tanzeem Rahat &nbsp;|&nbsp; **Submitted:** 3 May 2025

### Research Questions

1. **RQ1** — Which areas in Dhaka have the highest average rental prices, and how large is the price gap?
2. **RQ2** — How strongly does property size (sqft) influence rent? Is there a linear relationship?
3. **RQ3** — How does bedroom count affect rent, and which category offers the best value (price/sqft)?

### Dataset

| Property | Detail |
|----------|--------|
| Source | [Kaggle — House Rent of Dhaka and Chittagong (bproperty)](https://www.kaggle.com/datasets/shoaibshahriar33/house-rent-of-dhaka-and-chittagong-bproperty) |
| Scope | Dhaka-only listings (filtered from 2,000+ rows) |
| Key columns | `Area`, `Beds`, `Sqft`, `Location`, `Rent` (BDT/month) |

### Data Cleaning Steps

- Removed rows with missing values (`dropna()`)
- Eliminated duplicate listings (`drop_duplicates()`)
- Converted `sqft` from string (with commas/text) to `float` via regex + `pd.to_numeric()`
- Coerced `rent` to numeric and removed non-numeric placeholders
- Filtered out zero/negative `sqft` values
- Removed extreme outliers using the **IQR method** (1.5 × IQR above Q3)

### Feature Engineering

| Feature | How Created | Purpose |
|---------|-------------|---------|
| `price_per_sqft` | `rent / sqft` | Normalises rent by size for fair area comparisons |
| `rent_category` | `pd.cut()` → Low / Medium / High / Luxury | Groups market tiers by affordability |
| `bedroom_group` | `pd.cut()` → Small / Medium / Large | Reduces noise in bedroom-count subgroup analysis |

### NumPy Computations

- **Z-scores** — Identified outlier listings (`z > 2`) using `np.mean` / `np.std`
- **Trend line** — Linear regression via `np.polyfit(sqft, rent, 1)` + `np.linspace` for plotting
- **Percentile analysis** — `np.percentile(rent, [25, 50, 75, 90])` for precise affordability thresholds
- **Min-max normalisation** — Scaled rent to 0–1 range for modelling readiness

### Key Findings

1. **Location is the primary rent driver** — Gulshan, Banani, and Baridhara sit far above the city-wide median
2. **Size and rent are positively correlated but not deterministic** — scatter around the trend line shows location is an independent co-driver
3. **Premium tiers charge more per sqft, not just more in total** — a genuine location/amenity premium beyond property size
4. **Distribution is right-skewed** — median is more representative than mean for typical renter experience
5. **A small cluster of extreme-rent properties** persists in premium zones (confirmed by z-score analysis)
6. **Low and Medium tier listings dominate** the Dhaka market; High/Luxury are a small fraction

### Visualisations

| Figure | Type | What it shows |
|--------|------|---------------|
| Fig 1 | Bar chart | Average rent by area — top 15 Dhaka neighbourhoods |
| Fig 2 | Scatter + trend line | Sqft vs Rent relationship with `np.polyfit` line |
| Fig 3 | Bar chart | Average rent by bedroom group (Small / Medium / Large) |
| Fig 4 | Bar chart | Average price per sqft by rent category |
| Fig 5 | Histogram | Rent distribution — right-skewed |
| Fig 6 | Box plot | Outlier detection — IQR and five-number summary |

### Notebook

> Full code, outputs, and chart exports available in Google Colab:
> [Open Notebook](https://colab.research.google.com/drive/1PDT1VsqQcj5FEInEWRgSPh8hGdJdltIu#scrollTo=data-analysis)

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?logo=matplotlib&logoColor=white)
![tkinter](https://img.shields.io/badge/tkinter-GUI-blue)
![JSON](https://img.shields.io/badge/Storage-JSON-yellow)

---

## 📄 References

- McKinney, W. (2022). *Python for Data Analysis* (3rd ed.). O'Reilly Media.
- Harris, C.R. et al. (2020). Array programming with NumPy. *Nature*, 585, 357–362.
- Hunter, J.D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science & Engineering*, 9(3), 90–95.
