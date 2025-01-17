import sqlite3
from datetime import datetime
import os

class Database:
    def __init__(self):
        # Check if database exists
        db_exists = os.path.exists('finance_tracker.db')
        
        # Connect to database
        self.conn = sqlite3.connect('finance_tracker.db')
        
        # If database didn't exist or needs update, create/recreate tables
        if not db_exists:
            self.create_tables()
        else:
            # Try to add user_id column to existing tables if needed
            self.upgrade_database()
    
    def upgrade_database(self):
        cursor = self.conn.cursor()
        try:
            # Check if users table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
            if not cursor.fetchone():
                # Drop existing tables and recreate with new schema
                cursor.execute("DROP TABLE IF EXISTS expenses")
                cursor.execute("DROP TABLE IF EXISTS budgets")
                cursor.execute("DROP TABLE IF EXISTS savings_goals")
                self.create_tables()
        except sqlite3.Error:
            # If any error occurs, recreate all tables
            cursor.execute("DROP TABLE IF EXISTS expenses")
            cursor.execute("DROP TABLE IF EXISTS budgets")
            cursor.execute("DROP TABLE IF EXISTS savings_goals")
            self.create_tables()
        finally:
            self.conn.commit()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT,
                created_at TEXT
            )
        ''')
        
        # Expenses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                date TEXT,
                category TEXT,
                amount REAL,
                description TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Budgets table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                category TEXT,
                amount REAL,
                period TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Savings goals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS savings_goals (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                name TEXT,
                target_amount REAL,
                current_amount REAL,
                target_date TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        self.conn.commit()
        
    def add_expense(self, user_id, category, amount, description):
        cursor = self.conn.cursor()
        date = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            INSERT INTO expenses (user_id, date, category, amount, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, date, category, amount, description))
        self.conn.commit()
        
    def get_expenses(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC', (user_id,))
        return cursor.fetchall() 
        
    def set_budget(self, user_id, category, amount, period):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO budgets (user_id, category, amount, period)
            VALUES (?, ?, ?, ?)
        ''', (user_id, category, amount, period))
        self.conn.commit()
        
    def get_budgets(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM budgets WHERE user_id = ?', (user_id,))
        return cursor.fetchall()
        
    def add_savings_goal(self, user_id, name, target_amount, current_amount, target_date):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO savings_goals (user_id, name, target_amount, current_amount, target_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, name, target_amount, current_amount, target_date))
        self.conn.commit()
        
    def get_savings_goals(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM savings_goals WHERE user_id = ?', (user_id,))
        return cursor.fetchall() 
        
    def register_user(self, username, password):
        cursor = self.conn.cursor()
        date = datetime.now().strftime('%Y-%m-%d')
        try:
            cursor.execute('INSERT INTO users (username, password, created_at) VALUES (?, ?, ?)',
                          (username, password, date))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Username already exists
        
    def login_user(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, username FROM users WHERE username = ? AND password = ?',
                      (username, password))
        return cursor.fetchone() 