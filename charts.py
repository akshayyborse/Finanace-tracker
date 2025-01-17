import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta

def check_matplotlib():
    try:
        import matplotlib
        return True
    except ImportError:
        return False

class Charts:
    def __init__(self, notebook, db, user_id):
        self.db = db
        self.user_id = user_id
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Charts")
        
        if not check_matplotlib():
            ttk.Label(self.frame, text="Please install matplotlib to view charts:\npip install matplotlib", 
                     justify="center").pack(pady=20)
            return
            
        # Store references to charts
        self.category_ax = None
        self.category_canvas = None
        self.trend_ax = None
        self.trend_canvas = None
        
        # Create tabs for different charts
        self.create_chart_tabs()
        
        # Update charts initially
        self.update_all_charts()
        
    def create_chart_tabs(self):
        self.chart_notebook = ttk.Notebook(self.frame)
        self.chart_notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Category breakdown chart
        self.create_category_chart()
        
        # Monthly trend chart
        self.create_monthly_trend_chart()
        
    def create_category_chart(self):
        category_frame = ttk.Frame(self.chart_notebook)
        self.chart_notebook.add(category_frame, text="Category Breakdown")
        
        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(8, 6))
        self.category_ax = ax
        canvas = FigureCanvasTkAgg(fig, master=category_frame)
        self.category_canvas = canvas
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Add refresh button
        ttk.Button(category_frame, text="Refresh", 
                  command=lambda: self.update_category_chart()).pack(pady=5)
        
        # Initial chart
        self.update_category_chart()
        
    def create_monthly_trend_chart(self):
        trend_frame = ttk.Frame(self.chart_notebook)
        self.chart_notebook.add(trend_frame, text="Monthly Trend")
        
        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(8, 6))
        self.trend_ax = ax
        canvas = FigureCanvasTkAgg(fig, master=trend_frame)
        self.trend_canvas = canvas
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Add refresh button
        ttk.Button(trend_frame, text="Refresh", 
                  command=lambda: self.update_trend_chart()).pack(pady=5)
        
        # Initial chart
        self.update_trend_chart()
    
    def update_all_charts(self):
        """Update all charts at once"""
        self.update_category_chart()
        self.update_trend_chart()
        
    def update_category_chart(self):
        if not self.category_ax:
            return
            
        try:
            # Clear previous chart
            self.category_ax.clear()
            
            # Get expense data from database with user_id
            expenses = self.db.get_expenses(self.user_id)
            
            # Process data for pie chart
            categories = {}
            for expense in expenses:
                # expense format: (id, user_id, date, category, amount, description)
                category = expense[3]  # category is at index 3
                amount = expense[4]    # amount is at index 4
                categories[category] = categories.get(category, 0) + amount
            
            if categories:
                self.category_ax.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%')
                self.category_ax.set_title("Expenses by Category")
            else:
                self.category_ax.text(0.5, 0.5, "No expense data available", 
                                    ha='center', va='center')
            
            # Redraw the canvas
            self.category_canvas.draw()
            
        except Exception as e:
            print(f"Error updating category chart: {e}")
    
    def update_trend_chart(self):
        if not self.trend_ax:
            return
            
        try:
            # Clear previous chart
            self.trend_ax.clear()
            
            # Get expense data from database with user_id
            expenses = self.db.get_expenses(self.user_id)
            
            # Process data for line chart
            monthly_totals = {}
            for expense in expenses:
                # expense format: (id, user_id, date, category, amount, description)
                date = datetime.strptime(expense[2], '%Y-%m-%d')
                month_key = date.strftime('%Y-%m')
                amount = expense[4]
                monthly_totals[month_key] = monthly_totals.get(month_key, 0) + amount
            
            if monthly_totals:
                months = sorted(monthly_totals.keys())
                totals = [monthly_totals[month] for month in months]
                
                self.trend_ax.plot(months, totals, marker='o', linestyle='-', linewidth=2)
                self.trend_ax.set_title("Monthly Expenses Trend")
                self.trend_ax.set_xlabel("Month")
                self.trend_ax.set_ylabel("Total Expenses ($)")
                plt.setp(self.trend_ax.xaxis.get_majorticklabels(), rotation=45)
                self.trend_ax.grid(True, linestyle='--', alpha=0.7)
                
                # Adjust layout to prevent label cutoff
                plt.tight_layout()
            else:
                self.trend_ax.text(0.5, 0.5, "No expense data available", 
                                 ha='center', va='center')
            
            # Redraw the canvas
            self.trend_canvas.draw()
            
        except Exception as e:
            print(f"Error updating trend chart: {e}") 