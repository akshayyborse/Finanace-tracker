import tkinter as tk
from tkinter import ttk, messagebox

class BudgetManager:
    def __init__(self, notebook, db, user_id):
        self.db = db
        self.user_id = user_id
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Budgets")
        
        # Create budget input form
        self.create_input_form()
        
        # Create budget list
        self.create_budget_list()
        # Update the list initially
        self.update_budget_list()
        
    def create_input_form(self):
        input_frame = ttk.LabelFrame(self.frame, text="Set Budget", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Category dropdown
        ttk.Label(input_frame, text="Category:").grid(row=0, column=0, padx=5, pady=5)
        self.category_var = tk.StringVar()
        categories = ["Groceries", "Entertainment", "Utilities", "Transport", "Other"]
        self.category_combo = ttk.Combobox(input_frame, textvariable=self.category_var, values=categories)
        self.category_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Amount entry
        ttk.Label(input_frame, text="Budget Amount:").grid(row=1, column=0, padx=5, pady=5)
        self.amount_var = tk.StringVar()
        self.amount_entry = ttk.Entry(input_frame, textvariable=self.amount_var)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Period dropdown
        ttk.Label(input_frame, text="Period:").grid(row=2, column=0, padx=5, pady=5)
        self.period_var = tk.StringVar()
        periods = ["Monthly", "Yearly"]
        self.period_combo = ttk.Combobox(input_frame, textvariable=self.period_var, values=periods)
        self.period_combo.grid(row=2, column=1, padx=5, pady=5)
        
        # Add button
        ttk.Button(input_frame, text="Set Budget", command=self.set_budget).grid(row=3, column=0, columnspan=2, pady=10)
        
    def create_budget_list(self):
        list_frame = ttk.LabelFrame(self.frame, text="Budget List", padding=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.tree = ttk.Treeview(list_frame, columns=("Category", "Amount", "Period", "Spent", "Remaining"), show="headings")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Budget Amount")
        self.tree.heading("Period", text="Period")
        self.tree.heading("Spent", text="Spent")
        self.tree.heading("Remaining", text="Remaining")
        
        self.tree.pack(fill="both", expand=True)
        
    def set_budget(self):
        try:
            amount = float(self.amount_var.get())
            category = self.category_var.get()
            period = self.period_var.get()
            
            if not all([category, period]):
                messagebox.showerror("Error", "Please fill in all fields")
                return
                
            # Pass user_id to set_budget
            self.db.set_budget(self.user_id, category, amount, period)
            self.update_budget_list()
            
            # Clear inputs
            self.amount_var.set("")
            self.category_var.set("")
            self.period_var.set("")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
            
    def update_budget_list(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Add budgets from database with user_id
        for budget in self.db.get_budgets(self.user_id):
            # Calculate spent amount for this category
            spent = self.calculate_spent(budget[2])  # budget[2] is category
            remaining = budget[3] - spent  # budget[3] is amount
            
            self.tree.insert("", "end", values=(
                budget[2],  # Category
                f"${budget[3]:.2f}",  # Budget Amount
                budget[4],  # Period
                f"${spent:.2f}",  # Spent
                f"${remaining:.2f}"  # Remaining
            ))
            
    def calculate_spent(self, category):
        expenses = self.db.get_expenses(self.user_id)
        total = 0
        for expense in expenses:
            if expense[3] == category:  # expense[3] is category
                total += expense[4]  # expense[4] is amount
        return total 