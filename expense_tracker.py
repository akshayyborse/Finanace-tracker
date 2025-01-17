import tkinter as tk
from tkinter import ttk, messagebox

class ExpenseTracker:
    def __init__(self, notebook, db, user_id):
        self.db = db
        self.user_id = user_id
        
        # Create expense tab
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Expenses")
        
        # Expense input form
        self.create_input_form()
        
        # Expense list
        self.create_expense_list()
        
    def create_input_form(self):
        input_frame = ttk.LabelFrame(self.frame, text="Add Expense", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Category dropdown
        ttk.Label(input_frame, text="Category:").grid(row=0, column=0, padx=5, pady=5)
        self.category_var = tk.StringVar()
        categories = ["Groceries", "Entertainment", "Utilities", "Transport", "Other"]
        self.category_combo = ttk.Combobox(input_frame, textvariable=self.category_var, values=categories)
        self.category_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Amount entry
        ttk.Label(input_frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
        self.amount_var = tk.StringVar()
        self.amount_entry = ttk.Entry(input_frame, textvariable=self.amount_var)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Description entry
        ttk.Label(input_frame, text="Description:").grid(row=2, column=0, padx=5, pady=5)
        self.description_var = tk.StringVar()
        self.description_entry = ttk.Entry(input_frame, textvariable=self.description_var)
        self.description_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Add button
        ttk.Button(input_frame, text="Add Expense", command=self.add_expense).grid(row=3, column=0, columnspan=2, pady=10)
        
    def create_expense_list(self):
        # Create treeview for expenses
        list_frame = ttk.LabelFrame(self.frame, text="Expense List", padding=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.tree = ttk.Treeview(list_frame, columns=("Date", "Category", "Amount", "Description"), show="headings")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Description", text="Description")
        
        self.tree.pack(fill="both", expand=True)
        self.update_expense_list()
        
    def add_expense(self):
        try:
            amount = float(self.amount_var.get())
            category = self.category_var.get()
            description = self.description_var.get()
            
            if not category:
                messagebox.showerror("Error", "Please select a category")
                return
                
            # Add the expense
            self.db.add_expense(self.user_id, category, amount, description)
            
            # Update the expense list
            self.update_expense_list()
            
            # Clear inputs
            self.amount_var.set("")
            self.category_var.set("")
            self.description_var.set("")
            
            # Notify about the update
            if hasattr(self, 'on_expense_added'):
                self.on_expense_added()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
            
    def update_expense_list(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Add expenses from database with user_id
        for expense in self.db.get_expenses(self.user_id):
            self.tree.insert("", "end", values=expense[2:])  # Skip id and user_id 