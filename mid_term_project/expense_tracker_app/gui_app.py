"""
gui_app.py - ExpenseApp UI Controller Class
Builds and manages the full tkinter GUI for the Expense Tracker.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from expense_manager import ExpenseManager
from storage import JsonStorage
from expense import Expense


# ─────────────────────── Colour palette ───────────────────────
BG_MAIN      = "#1e1e2e"   # dark navy background
BG_CARD      = "#2a2a3e"   # slightly lighter card surface
BG_SIDEBAR   = "#16213e"   # sidebar/panel background
ACCENT       = "#7c6af7"   # purple accent (buttons, highlights)
ACCENT_HOVER = "#9b8ff9"
TEXT_MAIN    = "#e0e0f0"   # primary text
TEXT_DIM     = "#8888aa"   # muted labels
TEXT_WHITE   = "#ffffff"
SUCCESS      = "#4caf8c"
ERROR_COL    = "#e05c6e"
ENTRY_BG     = "#30304a"
BORDER       = "#3a3a5c"
ROW_ODD      = "#252538"
ROW_EVEN     = "#2a2a3e"
HEADER_BG    = "#7c6af7"

FONT_TITLE   = ("Segoe UI", 20, "bold")
FONT_HEAD    = ("Segoe UI", 13, "bold")
FONT_BODY    = ("Segoe UI", 11)
FONT_SMALL   = ("Segoe UI", 9)
FONT_LABEL   = ("Segoe UI", 10)


class ExpenseApp:
    """
    Main UI Controller class for the Expense Tracker desktop application.
    Uses composition with ExpenseManager for all business logic.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("💰 Expense Tracker")
        self.root.geometry("1100x680")
        self.root.minsize(900, 600)
        self.root.configure(bg=BG_MAIN)

        # Compose with manager (which composes with storage)
        self.manager = ExpenseManager(JsonStorage("data.json"))

        # State
        self.selected_id = None       # ID of the currently selected expense
        self.current_view = []        # Current visible list (after search/filter)

        self._build_ui()
        self._refresh_table(self.manager.get_all())

    # --------------------- UI BUILD ---------------------

    def _build_ui(self):
        """Build the full application layout."""
        self._build_top_bar()

        # Main container
        container = tk.Frame(self.root, bg=BG_MAIN)
        container.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # Left panel: form + controls
        self._build_left_panel(container)

        # Right panel: table + reports
        self._build_right_panel(container)

    def _build_top_bar(self):
        """Build the top header bar."""
        bar = tk.Frame(self.root, bg=BG_SIDEBAR, height=60)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        tk.Label(bar, text="💰 Expense Tracker",
                 font=FONT_TITLE, bg=BG_SIDEBAR,
                 fg=TEXT_WHITE).pack(side="left", padx=20, pady=10)

        # Date display
        today = date.today().strftime("%A, %d %B %Y")
        tk.Label(bar, text=today, font=FONT_SMALL,
                 bg=BG_SIDEBAR, fg=TEXT_DIM).pack(side="right", padx=20)

    def _build_left_panel(self, parent):
        """Build the left side panel with the expense form."""
        left = tk.Frame(parent, bg=BG_SIDEBAR, width=300)
        left.pack(side="left", fill="y", padx=(0, 8), pady=8)
        left.pack_propagate(False)

        # Form title
        tk.Label(left, text="Add / Edit Expense",
                 font=FONT_HEAD, bg=BG_SIDEBAR, fg=TEXT_WHITE
                 ).pack(pady=(18, 10), padx=15, anchor="w")

        tk.Frame(left, bg=BORDER, height=1).pack(fill="x", padx=15, pady=4)

        form_frame = tk.Frame(left, bg=BG_SIDEBAR)
        form_frame.pack(fill="x", padx=15)

        # Title field
        self._form_label(form_frame, "Title")
        self.entry_title = self._styled_entry(form_frame)

        # Category dropdown
        self._form_label(form_frame, "Category")
        self.combo_category = ttk.Combobox(
            form_frame, values=Expense.CATEGORIES,
            font=FONT_BODY, state="readonly"
        )
        self.combo_category.set(Expense.CATEGORIES[0])
        self._style_combobox(self.combo_category)
        self.combo_category.pack(fill="x", pady=(0, 10))

        # Amount field
        self._form_label(form_frame, "Amount (৳)")
        self.entry_amount = self._styled_entry(form_frame)

        # Date field
        self._form_label(form_frame, "Date (YYYY-MM-DD)")
        self.entry_date = self._styled_entry(form_frame)
        self.entry_date.insert(0, date.today().strftime("%Y-%m-%d"))

        tk.Frame(left, bg=BORDER, height=1).pack(fill="x", padx=15, pady=10)

        # Action buttons
        btn_frame = tk.Frame(left, bg=BG_SIDEBAR)
        btn_frame.pack(fill="x", padx=15)

        self._btn(btn_frame, "➕  Add Expense",   ACCENT,     self._on_add).pack(fill="x", pady=3)
        self._btn(btn_frame, "✏️  Update Expense", "#3a7bd5",  self._on_update).pack(fill="x", pady=3)
        self._btn(btn_frame, "🗑️  Delete Expense", ERROR_COL,  self._on_delete).pack(fill="x", pady=3)
        self._btn(btn_frame, "✖  Clear Form",     "#555570",  self._clear_form).pack(fill="x", pady=3)

        tk.Frame(left, bg=BORDER, height=1).pack(fill="x", padx=15, pady=10)

        # Search & filter
        tk.Label(left, text="Search & Filter",
                 font=FONT_HEAD, bg=BG_SIDEBAR, fg=TEXT_WHITE
                 ).pack(padx=15, anchor="w", pady=(0, 6))

        sf = tk.Frame(left, bg=BG_SIDEBAR)
        sf.pack(fill="x", padx=15)

        self._form_label(sf, "Search keyword")
        self.entry_search = self._styled_entry(sf)
        self._btn(sf, "🔍  Search", ACCENT, self._on_search).pack(fill="x", pady=3)

        self._form_label(sf, "Filter by Category")
        filter_cats = ["All"] + Expense.CATEGORIES
        self.combo_filter = ttk.Combobox(sf, values=filter_cats,
                                         font=FONT_BODY, state="readonly")
        self.combo_filter.set("All")
        self._style_combobox(self.combo_filter)
        self.combo_filter.pack(fill="x", pady=(0, 4))
        self.combo_filter.bind("<<ComboboxSelected>>", lambda e: self._on_filter())

        self._btn(sf, "↺  Show All", "#555570", self._on_show_all).pack(fill="x", pady=3)

        # Sort controls
        tk.Frame(left, bg=BORDER, height=1).pack(fill="x", padx=15, pady=10)
        sort_row = tk.Frame(left, bg=BG_SIDEBAR)
        sort_row.pack(fill="x", padx=15)

        tk.Label(sort_row, text="Sort by:", font=FONT_LABEL,
                 bg=BG_SIDEBAR, fg=TEXT_DIM).pack(side="left")

        self.combo_sort = ttk.Combobox(
            sort_row, values=["date", "amount", "title"],
            font=FONT_BODY, state="readonly", width=8
        )
        self.combo_sort.set("date")
        self._style_combobox(self.combo_sort)
        self.combo_sort.pack(side="left", padx=6)

        self.sort_desc = tk.BooleanVar(value=True)
        tk.Checkbutton(sort_row, text="Desc", variable=self.sort_desc,
                       bg=BG_SIDEBAR, fg=TEXT_DIM,
                       activebackground=BG_SIDEBAR,
                       selectcolor=ENTRY_BG, font=FONT_SMALL
                       ).pack(side="left")

        self._btn(left, "⇅  Sort", "#3a7bd5",
                  self._on_sort).pack(fill="x", padx=15, pady=4)

    def _build_right_panel(self, parent):
        """Build the right panel: expense table + report section."""
        right = tk.Frame(parent, bg=BG_MAIN)
        right.pack(side="left", fill="both", expand=True, pady=8)

        # ── Table section ──
        table_card = tk.Frame(right, bg=BG_CARD, bd=0)
        table_card.pack(fill="both", expand=True)

        hdr = tk.Frame(table_card, bg=BG_CARD)
        hdr.pack(fill="x", padx=15, pady=(12, 6))
        tk.Label(hdr, text="Expenses", font=FONT_HEAD,
                 bg=BG_CARD, fg=TEXT_WHITE).pack(side="left")
        self.label_count = tk.Label(hdr, text="0 records",
                                    font=FONT_SMALL, bg=BG_CARD, fg=TEXT_DIM)
        self.label_count.pack(side="right")

        # Treeview
        cols = ("ID", "Title", "Category", "Amount (৳)", "Date")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview",
                        background=ROW_ODD, foreground=TEXT_MAIN,
                        fieldbackground=ROW_ODD, rowheight=28,
                        font=FONT_BODY, borderwidth=0)
        style.configure("Custom.Treeview.Heading",
                        background=HEADER_BG, foreground=TEXT_WHITE,
                        font=("Segoe UI", 10, "bold"), relief="flat")
        style.map("Custom.Treeview",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", TEXT_WHITE)])

        tree_frame = tk.Frame(table_card, bg=BG_CARD)
        tree_frame.pack(fill="both", expand=True, padx=15, pady=(0, 12))

        self.tree = ttk.Treeview(tree_frame, columns=cols,
                                  show="headings", style="Custom.Treeview")
        widths = [50, 220, 130, 110, 110]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center" if col != "Title" else "w")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical",
                                   command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self._on_row_select)

        # ── Report section ──
        self._build_report_bar(right)

    def _build_report_bar(self, parent):
        """Build the summary report bar at the bottom."""
        report_card = tk.Frame(parent, bg=BG_CARD, height=110)
        report_card.pack(fill="x", pady=(8, 0))
        report_card.pack_propagate(False)

        tk.Label(report_card, text="📊  Summary Report",
                 font=FONT_HEAD, bg=BG_CARD, fg=TEXT_WHITE
                 ).pack(side="top", anchor="w", padx=15, pady=(10, 6))

        stats_frame = tk.Frame(report_card, bg=BG_CARD)
        stats_frame.pack(fill="x", padx=15)

        # Stat boxes
        self.stat_total    = self._stat_box(stats_frame, "Total",    "৳0.00")
        self.stat_avg      = self._stat_box(stats_frame, "Average",  "৳0.00")
        self.stat_highest  = self._stat_box(stats_frame, "Highest",  "৳0.00")
        self.stat_count    = self._stat_box(stats_frame, "Records",  "0")
        self.btn_full_report = self._btn(
            stats_frame, "Full Report", ACCENT, self._show_full_report
        )
        self.btn_full_report.pack(side="left", padx=(12, 0), pady=4)

        self._update_report()

    # ═══════════════════════ HELPER WIDGETS ═════════════════════════

    def _form_label(self, parent, text):
        tk.Label(parent, text=text, font=FONT_LABEL,
                 bg=BG_SIDEBAR, fg=TEXT_DIM).pack(anchor="w", pady=(6, 2))

    def _styled_entry(self, parent):
        e = tk.Entry(parent, bg=ENTRY_BG, fg=TEXT_MAIN,
                     insertbackground=TEXT_MAIN, font=FONT_BODY,
                     relief="flat", bd=6)
        e.pack(fill="x", pady=(0, 2))
        return e

    def _style_combobox(self, combo):
        combo.configure(background=ENTRY_BG)

    def _btn(self, parent, text, color, command):
        b = tk.Button(parent, text=text, bg=color, fg=TEXT_WHITE,
                      activebackground=ACCENT_HOVER, activeforeground=TEXT_WHITE,
                      font=FONT_BODY, relief="flat", cursor="hand2",
                      padx=8, pady=6, command=command)
        b.bind("<Enter>", lambda e: b.config(bg=ACCENT_HOVER))
        b.bind("<Leave>", lambda e: b.config(bg=color))
        return b

    def _stat_box(self, parent, label, value):
        box = tk.Frame(parent, bg=BG_SIDEBAR, padx=14, pady=6)
        box.pack(side="left", padx=(0, 8))
        tk.Label(box, text=label, font=FONT_SMALL,
                 bg=BG_SIDEBAR, fg=TEXT_DIM).pack(anchor="w")
        val_label = tk.Label(box, text=value, font=("Segoe UI", 12, "bold"),
                             bg=BG_SIDEBAR, fg=ACCENT)
        val_label.pack(anchor="w")
        return val_label

    # ═══════════════════════ TABLE MANAGEMENT ═══════════════════════

    def _refresh_table(self, expenses: list):
        """Clear and repopulate the treeview with the given expense list."""
        self.current_view = expenses
        for row in self.tree.get_children():
            self.tree.delete(row)

        for i, exp in enumerate(expenses):
            tag = "odd" if i % 2 == 0 else "even"
            self.tree.insert("", "end", iid=str(exp.id), tags=(tag,),
                             values=(exp.id, exp.title, exp.category,
                                     f"৳{exp.amount:,.2f}", exp.date))

        self.tree.tag_configure("odd",  background=ROW_ODD)
        self.tree.tag_configure("even", background=ROW_EVEN)

        self.label_count.config(text=f"{len(expenses)} record(s)")
        self._update_report()

    def _update_report(self):
        """Refresh the summary stats from the manager."""
        r = self.manager.get_report()
        self.stat_total.config(text=f"৳{r['total']:,.2f}")
        self.stat_avg.config(text=f"৳{r['average']:,.2f}")
        highest_amt = r['highest'].amount if r['highest'] else 0
        self.stat_highest.config(text=f"৳{highest_amt:,.2f}")
        self.stat_count.config(text=str(r['count']))


    # --------------------- FORM HELPERS ---------------------

    def _get_form_values(self):
        return (
            self.entry_title.get(),
            self.combo_category.get(),
            self.entry_amount.get(),
            self.entry_date.get()
        )

    def _clear_form(self):
        """Reset all form fields and deselect table row."""
        self.selected_id = None
        self.entry_title.delete(0, tk.END)
        self.combo_category.set(Expense.CATEGORIES[0])
        self.entry_amount.delete(0, tk.END)
        self.entry_date.delete(0, tk.END)
        self.entry_date.insert(0, date.today().strftime("%Y-%m-%d"))
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())

    def _populate_form(self, expense):
        """Fill the form fields from an Expense object."""
        self.entry_title.delete(0, tk.END)
        self.entry_title.insert(0, expense.title)
        self.combo_category.set(expense.category)
        self.entry_amount.delete(0, tk.END)
        self.entry_amount.insert(0, str(expense.amount))
        self.entry_date.delete(0, tk.END)
        self.entry_date.insert(0, expense.date)

    def _show_msg(self, success: bool, msg: str):
        if success:
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)

    # --------------------- EVENT HANDLERS ---------------------

    def _on_row_select(self, event):
        """When user clicks a table row, load its data into the form."""
        selected = self.tree.selection()
        if not selected:
            return
        expense_id = int(selected[0])
        expense = self.manager.get_by_id(expense_id)
        if expense:
            self.selected_id = expense_id
            self._populate_form(expense)

    def _on_add(self):
        title, category, amount, exp_date = self._get_form_values()
        success, msg = self.manager.add_expense(title, category, amount, exp_date)
        self._show_msg(success, msg)
        if success:
            self._refresh_table(self.manager.get_all())
            self._clear_form()

    def _on_update(self):
        if self.selected_id is None:
            messagebox.showwarning("No Selection",
                                   "Please select an expense from the table to update.")
            return
        title, category, amount, exp_date = self._get_form_values()
        success, msg = self.manager.update_expense(
            self.selected_id, title, category, amount, exp_date
        )
        self._show_msg(success, msg)
        if success:
            self._refresh_table(self.manager.get_all())
            self._clear_form()

    def _on_delete(self):
        if self.selected_id is None:
            messagebox.showwarning("No Selection",
                                   "Please select an expense from the table to delete.")
            return
        expense = self.manager.get_by_id(self.selected_id)
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{expense.title}'?"
        )
        if not confirm:
            return
        success, msg = self.manager.delete_expense(self.selected_id)
        self._show_msg(success, msg)
        if success:
            self._refresh_table(self.manager.get_all())
            self._clear_form()

    def _on_search(self):
        keyword = self.entry_search.get()
        results = self.manager.search(keyword)
        if not results:
            messagebox.showinfo("Search", f"No results found for '{keyword}'.")
        self._refresh_table(results)

    def _on_filter(self):
        cat = self.combo_filter.get()
        results = self.manager.filter_by_category(cat)
        self._refresh_table(results)

    def _on_sort(self):
        field = self.combo_sort.get()
        desc = self.sort_desc.get()
        sorted_list = self.manager.sort_by(self.current_view, field, desc)
        self._refresh_table(sorted_list)

    def _on_show_all(self):
        self.entry_search.delete(0, tk.END)
        self.combo_filter.set("All")
        self._refresh_table(self.manager.get_all())

    def _show_full_report(self):
        """Open a popup window with the full category-wise report."""
        r = self.manager.get_report()

        win = tk.Toplevel(self.root)
        win.title("📊 Full Expense Report")
        win.geometry("460x500")
        win.configure(bg=BG_MAIN)
        win.resizable(False, False)

        tk.Label(win, text="📊  Full Expense Report",
                 font=FONT_TITLE, bg=BG_MAIN, fg=TEXT_WHITE
                 ).pack(pady=(20, 6), padx=20, anchor="w")
        tk.Frame(win, bg=BORDER, height=1).pack(fill="x", padx=20, pady=6)

        # Summary stats
        stats = [
            ("Total Expenses",    f"৳{r['total']:,.2f}"),
            ("Number of Records", str(r['count'])),
            ("Average Expense",   f"৳{r['average']:,.2f}"),
            ("Highest Expense",
             f"৳{r['highest'].amount:,.2f} ({r['highest'].title})"
             if r['highest'] else "N/A"),
            ("Lowest Expense",
             f"৳{r['lowest'].amount:,.2f} ({r['lowest'].title})"
             if r['lowest'] else "N/A"),
        ]
        for label, value in stats:
            row = tk.Frame(win, bg=BG_CARD, pady=6, padx=14)
            row.pack(fill="x", padx=20, pady=2)
            tk.Label(row, text=label, font=FONT_BODY,
                     bg=BG_CARD, fg=TEXT_DIM, width=22, anchor="w"
                     ).pack(side="left")
            tk.Label(row, text=value, font=("Segoe UI", 11, "bold"),
                     bg=BG_CARD, fg=ACCENT).pack(side="right")

        # Category breakdown
        tk.Frame(win, bg=BORDER, height=1).pack(fill="x", padx=20, pady=10)
        tk.Label(win, text="Category Breakdown",
                 font=FONT_HEAD, bg=BG_MAIN, fg=TEXT_WHITE
                 ).pack(padx=20, anchor="w", pady=(0, 6))

        if r["category_totals"]:
            sorted_cats = sorted(r["category_totals"].items(),
                                 key=lambda x: x[1], reverse=True)
            for cat, total in sorted_cats:
                row = tk.Frame(win, bg=BG_CARD, pady=5, padx=14)
                row.pack(fill="x", padx=20, pady=2)
                tk.Label(row, text=cat, font=FONT_BODY,
                         bg=BG_CARD, fg=TEXT_MAIN, width=18, anchor="w"
                         ).pack(side="left")
                pct = (total / r["total"] * 100) if r["total"] > 0 else 0
                tk.Label(row, text=f"৳{total:,.2f}  ({pct:.1f}%)",
                         font=("Segoe UI", 11, "bold"),
                         bg=BG_CARD, fg=SUCCESS).pack(side="right")
        else:
            tk.Label(win, text="No data available.",
                     font=FONT_BODY, bg=BG_MAIN, fg=TEXT_DIM).pack(pady=10)

        self._btn(win, "Close", "#555570", win.destroy).pack(pady=16)
