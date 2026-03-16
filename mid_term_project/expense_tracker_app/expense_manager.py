"""
expense_manager.py - ExpenseManager Service Class
Handles all business logic for expense operations.
"""

from expense import Expense
from storage import JsonStorage


class ExpenseManager:
    """
    Manager/Service class that handles all expense operations.
    Uses composition with JsonStorage for persistence.

    Attributes:
        storage (JsonStorage): Storage handler instance.
        expenses (list): In-memory list of Expense objects.
    """

    def __init__(self, storage: JsonStorage):
        self.storage = storage
        self.expenses = self.storage.load()

    # -------------------------- CRUD --------------------------

    """ Add Expense """
    def add_expense(self, title: str, category: str,
                    amount: str, expense_date: str) -> tuple:

        error = Expense.validate(title, category, amount, expense_date)
        if error:
            return False, error

        new_id = self.storage.get_next_id(self.expenses)
        expense = Expense(new_id, title, category, float(amount), expense_date)
        self.expenses.append(expense)
        self.storage.save(self.expenses)
        return True, f"Expense '{title}' added successfully."

    """ Update Expense """
    def update_expense(self, expense_id: int, title: str, category: str,
                       amount: str, expense_date: str) -> tuple:

        error = Expense.validate(title, category, amount, expense_date)
        if error:
            return False, error

        for expense in self.expenses:
            if expense.id == expense_id:
                expense.title = title.strip()
                expense.category = category.strip()
                expense.amount = float(amount)
                expense.date = expense_date.strip()
                self.storage.save(self.expenses)
                return True, f"Expense updated successfully."

        return False, f"Expense with ID: {expense_id} not found."

    """ Delete Expense """
    def delete_expense(self, expense_id: int) -> tuple:

        for expense in self.expenses:
            if expense.id == expense_id:
                self.expenses.remove(expense)
                self.storage.save(self.expenses)
                return True, f"Expense '{expense.title}' deleted."

        return False, f"Expense with ID: {expense_id} not found."

    """ Get All Expense """
    def get_all(self) -> list:
        return self.expenses

    """ Get Single Expense by ID """
    def get_by_id(self, expense_id: int):
        for expense in self.expenses:
            if expense.id == expense_id:
                return expense
        return None

    # ────────────────────── SEARCH / FILTER ──────────────────────

    """ Search expenses by title or category """
    def search(self, keyword: str) -> list:

        keyword = keyword.strip().lower()
        if not keyword:
            return self.expenses
        return [
            e for e in self.expenses
            if keyword in e.title.lower() or keyword in e.category.lower()
        ]

    """ Filter expenses by exact category match. """
    def filter_by_category(self, category: str) -> list:
        
        if category == "All":
            return self.expenses
        return [e for e in self.expenses if e.category == category]

    """ Sort expenses by a given field (date, amount, title) """
    def sort_by(self, expenses: list, field: str, descending: bool = False) -> list:
        
        valid_fields = {"amount", "date", "title"}
        if field not in valid_fields:
            return expenses
        return sorted(expenses, key=lambda e: getattr(e, field),
                      reverse=descending)

    # ──────────────────────── REPORTS ────────────────────────────

    def get_report(self) -> dict:
        """
        Generate a summary report of all expenses.

        Returns:
            dict: Report data with totals, averages, and category breakdown.
        """
        if not self.expenses:
            return {
                "total": 0.0,
                "average": 0.0,
                "highest": None,
                "lowest": None,
                "count": 0,
                "category_totals": {}
            }

        amounts = [e.amount for e in self.expenses]
        total = sum(amounts)
        average = total / len(amounts)
        highest = max(self.expenses, key=lambda e: e.amount)
        lowest = min(self.expenses, key=lambda e: e.amount)

        category_totals = {}
        for e in self.expenses:
            category_totals[e.category] = (
                category_totals.get(e.category, 0.0) + e.amount
            )

        return {
            "total": round(total, 2),
            "average": round(average, 2),
            "highest": highest,
            "lowest": lowest,
            "count": len(self.expenses),
            "category_totals": category_totals
        }
