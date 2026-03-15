"""
expense.py - Expense Entity Class
Represents a single expense record.
"""

from datetime import date


class Expense:
    """
    Entity class representing a single expense record.

    Attributes:
        id (int): Unique identifier
        title (str): Name/description of the expense
        category (str): Category of the expense (Food, Transport, etc.)
        amount (float): Amount spent
        date (str): Date of expense in YYYY-MM-DD format
    """

    CATEGORIES = ["Food", "Transport", "Shopping", "Health", "Education",
                  "Entertainment", "Bills", "Other"]

    # Constructor crate & Assign values
    def __init__(self, expense_id: int, title: str, category: str,
                 amount: float, expense_date: str):
        self.id = expense_id
        self.title = title.strip()
        self.category = category.strip()
        self.amount = float(amount)
        self.date = expense_date

    # Convert Object to Dictionary
    def to_dict(self) -> dict:
        """Convert the Expense object to a dictionary for JSON storage."""
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "amount": self.amount,
            "date": self.date
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Expense":
        """Create an Expense object from a dictionary (loaded from JSON)."""
        return cls(
            expense_id=data["id"],
            title=data["title"],
            category=data["category"],
            amount=data["amount"],
            expense_date=data["date"]
        )

    @staticmethod
    def validate(title: str, category: str, amount: str, expense_date: str) -> str:
        """
        Validate expense fields before creation.

        Returns:
            str: Error message if invalid, empty string if valid.
        """
        if not title.strip():
            return "Title cannot be empty."
        if not category.strip():
            return "Category cannot be empty."
        if not expense_date.strip():
            return "Date cannot be empty."
        try:
            amt = float(amount)
            if amt <= 0:
                return "Amount must be greater than zero."
        except ValueError:
            return "Amount must be a valid number."
        try:
            parts = expense_date.strip().split("-")
            if len(parts) != 3:
                raise ValueError
            date(int(parts[0]), int(parts[1]), int(parts[2]))
        except (ValueError, IndexError):
            return "Date must be in YYYY-MM-DD format (e.g. 2026-03-14)."
        return ""

    def __repr__(self):
        return f"Expense(id={self.id}, title='{self.title}', amount={self.amount})"
