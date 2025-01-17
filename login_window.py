import tkinter as tk
from tkinter import ttk, messagebox
import hashlib

class LoginWindow:
    def __init__(self, db, on_login_success):
        self.db = db
        self.on_login_success = on_login_success
        
        self.root = tk.Tk()
        self.root.title("Finance Tracker - Login")
        self.root.geometry("300x400")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Login Frame
        login_frame = ttk.LabelFrame(self.root, text="Login", padding=20)
        login_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Username
        ttk.Label(login_frame, text="Username:").pack(fill="x", pady=5)
        self.username_var = tk.StringVar()
        ttk.Entry(login_frame, textvariable=self.username_var).pack(fill="x", pady=5)
        
        # Password
        ttk.Label(login_frame, text="Password:").pack(fill="x", pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(login_frame, textvariable=self.password_var, show="*").pack(fill="x", pady=5)
        
        # Login button
        ttk.Button(login_frame, text="Login", command=self.login).pack(fill="x", pady=20)
        
        # Register link
        ttk.Label(login_frame, text="Don't have an account?").pack(pady=5)
        ttk.Button(login_frame, text="Register", command=self.show_register).pack()
        
    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        # Hash password (in real app, use better security)
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        user = self.db.login_user(username, hashed_password)
        if user:
            self.root.destroy()
            self.on_login_success(user[0], user[1])  # Pass user_id and username
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def show_register(self):
        register_window = RegisterWindow(self.db)
        
    def run(self):
        self.root.mainloop()

class RegisterWindow:
    def __init__(self, db):
        self.db = db
        
        self.root = tk.Toplevel()
        self.root.title("Register")
        self.root.geometry("300x400")
        
        self.create_widgets()
        
    def create_widgets(self):
        register_frame = ttk.LabelFrame(self.root, text="Register", padding=20)
        register_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Username
        ttk.Label(register_frame, text="Username:").pack(fill="x", pady=5)
        self.username_var = tk.StringVar()
        ttk.Entry(register_frame, textvariable=self.username_var).pack(fill="x", pady=5)
        
        # Password
        ttk.Label(register_frame, text="Password:").pack(fill="x", pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(register_frame, textvariable=self.password_var, show="*").pack(fill="x", pady=5)
        
        # Confirm Password
        ttk.Label(register_frame, text="Confirm Password:").pack(fill="x", pady=5)
        self.confirm_var = tk.StringVar()
        ttk.Entry(register_frame, textvariable=self.confirm_var, show="*").pack(fill="x", pady=5)
        
        # Register button
        ttk.Button(register_frame, text="Register", command=self.register).pack(fill="x", pady=20)
        
    def register(self):
        username = self.username_var.get()
        password = self.password_var.get()
        confirm = self.confirm_var.get()
        
        if not all([username, password, confirm]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
            
        # Hash password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        if self.db.register_user(username, hashed_password):
            messagebox.showinfo("Success", "Registration successful! You can now login.")
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Username already exists") 