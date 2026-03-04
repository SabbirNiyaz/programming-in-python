import tkinter as tk
from tkinter import messagebox
import json
import os

# --------------------------
# 1️⃣ Entity Class
# --------------------------
class Expense:
    def __init__(self, title, category, amount):
        self.title = title
        self.category = category
        self.amount = float(amount)

    def to_dict(self):
        return {
            "title": self.title,
            "category": self.category,
            "amount": self.amount
        }


# --------------------------
# 2️⃣ Storage Class
# --------------------------
class JsonStorage:
    def __init__(self, filename="data.json"):
        self.filename = filename

    def save(self, expenses):
        with open(self.filename, "w") as f:
            json.dump([e.to_dict() for e in expenses], f, indent=4)

    def load(self):
        if not os.path.exists(self.filename):
            return []

        with open(self.filename, "r") as f:
            data = json.load(f)
            return [Expense(d["title"], d["category"], d["amount"]) for d in data]


# --------------------------
# 3️⃣ Manager Class
# --------------------------
class ExpenseManager:
    def __init__(self, storage):
        self.storage = storage
        self.expenses = self.storage.load()

    def add_expense(self, title, category, amount):
        expense = Expense(title, category, amount)
        self.expenses.append(expense)
        self.storage.save(self.expenses)

    def delete_expense(self, index):
        if 0 <= index < len(self.expenses):
            self.expenses.pop(index)
            self.storage.save(self.expenses)

    def get_total(self):
        return sum(e.amount for e in self.expenses)

    def search(self, keyword):
        return [e for e in self.expenses if keyword.lower() in e.title.lower()]


# --------------------------
# 4️⃣ GUI Controller (Styled Only)
# --------------------------
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 Expense Tracker")
        self.root.geometry("500x600")
        self.root.configure(bg="#f0f4f8")

        self.manager = ExpenseManager(JsonStorage())

        # --------- HEADER ----------
        tk.Label(
            root,
            text="Expense Tracker",
            font=("Segoe UI", 20, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=15
        ).pack(fill="x")

        # --------- FORM SECTION ----------
        form_frame = tk.Frame(root, bg="#f0f4f8")
        form_frame.pack(pady=15)

        # Title
        tk.Label(form_frame, text="Title",
                 font=("Segoe UI", 10, "bold"),
                 bg="#f0f4f8").pack(anchor="w")
        self.title_entry = tk.Entry(form_frame,
                                    font=("Segoe UI", 11),
                                    width=35,
                                    bd=2,
                                    relief="groove")
        self.title_entry.pack(pady=5)

        # Category
        tk.Label(form_frame, text="Category",
                 font=("Segoe UI", 10, "bold"),
                 bg="#f0f4f8").pack(anchor="w")
        self.category_entry = tk.Entry(form_frame,
                                       font=("Segoe UI", 11),
                                       width=35,
                                       bd=2,
                                       relief="groove")
        self.category_entry.pack(pady=5)

        # Amount
        tk.Label(form_frame, text="Amount",
                 font=("Segoe UI", 10, "bold"),
                 bg="#f0f4f8").pack(anchor="w")
        self.amount_entry = tk.Entry(form_frame,
                                     font=("Segoe UI", 11),
                                     width=35,
                                     bd=2,
                                     relief="groove")
        self.amount_entry.pack(pady=5)

        # --------- BUTTONS ----------
        tk.Button(root,
                  text="➕ Add Expense",
                  font=("Segoe UI", 10, "bold"),
                  bg="#27ae60",
                  fg="white",
                  activebackground="#2ecc71",
                  width=25,
                  command=self.add_expense).pack(pady=5)

        tk.Button(root,
                  text="🗑 Delete Selected",
                  font=("Segoe UI", 10, "bold"),
                  bg="#e74c3c",
                  fg="white",
                  activebackground="#c0392b",
                  width=25,
                  command=self.delete_expense).pack(pady=5)

        tk.Button(root,
                  text="📊 Show Total",
                  font=("Segoe UI", 10, "bold"),
                  bg="#2980b9",
                  fg="white",
                  activebackground="#3498db",
                  width=25,
                  command=self.show_total).pack(pady=5)

        # --------- SEARCH ----------
        tk.Label(root,
                 text="Search",
                 font=("Segoe UI", 10, "bold"),
                 bg="#f0f4f8").pack(pady=(15, 0))

        self.search_entry = tk.Entry(root,
                                     font=("Segoe UI", 11),
                                     width=35,
                                     bd=2,
                                     relief="groove")
        self.search_entry.pack(pady=5)

        tk.Button(root,
                  text="🔍 Search",
                  font=("Segoe UI", 10, "bold"),
                  bg="#8e44ad",
                  fg="white",
                  activebackground="#9b59b6",
                  width=25,
                  command=self.search_expense).pack(pady=5)

        # --------- LISTBOX ----------
        self.listbox = tk.Listbox(
            root,
            width=55,
            height=10,
            font=("Consolas", 10),
            bg="white",
            fg="#2c3e50",
            bd=2,
            relief="ridge",
            selectbackground="#3498db",
            selectforeground="white"
        )
        self.listbox.pack(pady=15)

        self.refresh_list()

    def add_expense(self):
        title = self.title_entry.get()
        category = self.category_entry.get()
        amount = self.amount_entry.get()

        if not title or not category or not amount:
            messagebox.showerror("Error", "All fields required!")
            return

        try:
            float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be number!")
            return

        self.manager.add_expense(title, category, amount)
        self.refresh_list()

        self.title_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

    def delete_expense(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Select an item to delete!")
            return

        self.manager.delete_expense(selected[0])
        self.refresh_list()

    def show_total(self):
        total = self.manager.get_total()
        messagebox.showinfo("Total Expense", f"Total: {total:.2f}")

    def search_expense(self):
        keyword = self.search_entry.get()
        results = self.manager.search(keyword)

        self.listbox.delete(0, tk.END)
        for e in results:
            self.listbox.insert(tk.END, f"{e.title} | {e.category} | {e.amount}")

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for e in self.manager.expenses:
            self.listbox.insert(tk.END, f"{e.title} | {e.category} | {e.amount}")


# --------------------------
# Run App
# --------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()