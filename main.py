import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from expense_tracker import ExpenseTracker
from budget_manager import BudgetManager
from savings_goals import SavingsGoals
from charts import Charts
from login_window import LoginWindow

class FinanceTrackerApp:
    def __init__(self):
        self.db = Database()
        
        # Start with login window
        self.login_window = LoginWindow(self.db, self.on_login_success)
        self.login_window.run()
        
    def on_login_success(self, user_id, username):
        self.user_id = user_id
        self.username = username
        
        self.root = tk.Tk()
        self.root.title(f"Personal Finance Tracker - {username}")
        self.root.geometry("800x600")
        
        # Create a frame for the logout button at the top
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        # Add logout button to the right
        ttk.Button(button_frame, text="Logout", command=self.logout).pack(side="right")
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True, fill="both")
        
        try:
            # Initialize different sections with user_id
            self.expense_tracker = ExpenseTracker(self.notebook, self.db, self.user_id)
            self.budget_manager = BudgetManager(self.notebook, self.db, self.user_id)
            self.savings_goals = SavingsGoals(self.notebook, self.db, self.user_id)
            self.charts = Charts(self.notebook, self.db, self.user_id)
            
            # Connect expense tracker to charts and budget manager
            self.expense_tracker.on_expense_added = self.on_expense_update
            
            # Select first tab
            self.notebook.select(0)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error initializing application: {str(e)}")
        
        self.root.mainloop()
        
    def on_expense_update(self):
        """Called when an expense is added or updated"""
        try:
            self.charts.update_all_charts()
            self.budget_manager.update_budget_list()
        except Exception as e:
            print(f"Error updating charts: {e}")
        
    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            self.__init__()  # Restart the application

if __name__ == "__main__":
    app = FinanceTrackerApp() 