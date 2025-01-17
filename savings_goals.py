import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class SavingsGoals:
    def __init__(self, notebook, db, user_id):
        self.db = db
        self.user_id = user_id
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Savings")
        
        # Create goal input form
        self.create_input_form()
        
        # Create goals list
        self.create_goals_list()
        # Update the list initially
        self.update_goals_list()
        
    def create_input_form(self):
        input_frame = ttk.LabelFrame(self.frame, text="Add Savings Goal", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Goal name
        ttk.Label(input_frame, text="Goal Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(input_frame, textvariable=self.name_var)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Target amount
        ttk.Label(input_frame, text="Target Amount:").grid(row=1, column=0, padx=5, pady=5)
        self.target_var = tk.StringVar()
        self.target_entry = ttk.Entry(input_frame, textvariable=self.target_var)
        self.target_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Current amount
        ttk.Label(input_frame, text="Current Amount:").grid(row=2, column=0, padx=5, pady=5)
        self.current_var = tk.StringVar()
        self.current_entry = ttk.Entry(input_frame, textvariable=self.current_var)
        self.current_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Target date
        ttk.Label(input_frame, text="Target Date (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5)
        self.date_var = tk.StringVar()
        self.date_entry = ttk.Entry(input_frame, textvariable=self.date_var)
        self.date_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Add button
        ttk.Button(input_frame, text="Add Goal", command=self.add_goal).grid(row=4, column=0, columnspan=2, pady=10)
        
    def create_goals_list(self):
        list_frame = ttk.LabelFrame(self.frame, text="Savings Goals", padding=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.tree = ttk.Treeview(list_frame, columns=("Name", "Target", "Current", "Progress", "Target Date"), show="headings")
        self.tree.heading("Name", text="Goal Name")
        self.tree.heading("Target", text="Target Amount")
        self.tree.heading("Current", text="Current Amount")
        self.tree.heading("Progress", text="Progress %")
        self.tree.heading("Target Date", text="Target Date")
        
        self.tree.pack(fill="both", expand=True)
        
    def add_goal(self):
        try:
            name = self.name_var.get().strip()
            target = float(self.target_var.get())
            current = float(self.current_var.get())
            date = self.date_var.get()

            # Validate inputs
            if not name:
                messagebox.showerror("Error", "Please enter a goal name")
                return
                
            if target <= 0:
                messagebox.showerror("Error", "Target amount must be greater than 0")
                return
                
            if current < 0:
                messagebox.showerror("Error", "Current amount cannot be negative")
                return
                
            try:
                datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
                return

            # Pass user_id to add_savings_goal
            self.db.add_savings_goal(self.user_id, name, target, current, date)

            # Clear entry fields
            self.name_var.set("")
            self.target_var.set("")
            self.current_var.set("")
            self.date_var.set("")

            # Update the display
            self.update_goals_list()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for amounts")
            
    def update_goals_list(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Add goals from database with user_id
        for goal in self.db.get_savings_goals(self.user_id):
            progress = (goal[4] / goal[3]) * 100 if goal[3] > 0 else 0
            self.tree.insert("", "end", values=(goal[2], goal[3], goal[4], f"{progress:.1f}%", goal[5]))