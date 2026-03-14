"""
main.py - Application Entry Point
Launches the Expense Tracker desktop application.

Usage:
    python main.py
"""

import tkinter as tk
from gui_app import ExpenseApp


def main():
    """Initialize and start the Expense Tracker application."""
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
