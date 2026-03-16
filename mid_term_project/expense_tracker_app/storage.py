"""
storage.py - JsonStorage Class
Handles all data persistence using JSON file.
"""

import json # reading/writing JSON files
import os # checking if the file exists
from expense import Expense # convert dictionaries back into Expense objects


class JsonStorage:
    """
    Storage class responsible for saving and loading expense data to/from a JSON file.

    Attributes:
        filepath (str): Path to the JSON data file.
    """

    def __init__(self, filepath: str = "data.json"):
        self.filepath = filepath

    def save(self, expenses: list) -> bool:
        """
        Save a list of Expense objects to the JSON file.

        Args:
            expenses (list): List of Expense objects to save.

        Returns:
            bool: True if saved successfully, False otherwise.
        """
        try:
            # Convert all Expense objects to dictionaries
            data = [e.to_dict() for e in expenses]
            
            # Open the file in write mode and dump JSON
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            return True
        except (IOError, OSError) as e:
            print(f"[Storage Error] Could not save data: {e}")
            return False

    def load(self) -> list:
        """
        Load expenses from the JSON file.

        Returns:
            list: List of Expense objects. Returns empty list if file doesn't exist.
        """
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Expense.from_dict(item) for item in data]
        except (json.JSONDecodeError, KeyError, IOError) as e:
            print(f"[Storage Error] Could not load data: {e}")
            return []

    def get_next_id(self, expenses: list) -> int:
        """
        Generate the next stable unique ID for a new expense.

        Args:
            expenses (list): Current list of expenses.

        Returns:
            int: Next available ID.
        """
        if not expenses:
            return 1
        return max(e.id for e in expenses) + 1
