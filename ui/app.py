import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from manager.password_gen import generate_password
from manager.manager import PasswordManager
import os

class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager&Generator")
        self.password_manager = None

        # Account selection screen
        self.account_frame = tk.Frame(root)
        self.account_frame.pack(pady=20)

        tk.Button(self.account_frame, text="Login", command=self.show_login).grid(row=0, column=0, padx=10)
        tk.Button(self.account_frame, text="Register Account", command=self.show_create_account).grid(row=0, column=1, padx=10)

    def show_login(self):
        self.account_frame.pack_forget()

        # Create login frame
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="Account Name:").grid(row=0, column=0)
        self.account_name_entry = tk.Entry(self.login_frame)
        self.account_name_entry.grid(row=0, column=1)

        tk.Label(self.login_frame, text="Master Password:").grid(row=1, column=0)
        self.master_password_entry = tk.Entry(self.login_frame, show="*")
        self.master_password_entry.grid(row=1, column=1)

        tk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(self.login_frame, text="Back", command=self.show_account_choice).grid(row=3, column=0, columnspan=2, pady=10)

    def show_create_account(self):
        self.account_frame.pack_forget()

        # Create account creation frame
        self.create_account_frame = tk.Frame(self.root)
        self.create_account_frame.pack(pady=20)

        tk.Label(self.create_account_frame, text="Account Name:").grid(row=0, column=0)
        self.new_account_name_entry = tk.Entry(self.create_account_frame)
        self.new_account_name_entry.grid(row=0, column=1)

        tk.Label(self.create_account_frame, text="Master Password:").grid(row=1, column=0)
        self.new_master_password_entry = tk.Entry(self.create_account_frame, show="*")
        self.new_master_password_entry.grid(row=1, column=1)

        tk.Button(self.create_account_frame, text="Create Account", command=self.create_account).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(self.create_account_frame, text="Back", command=self.show_account_choice).grid(row=3, column=0, columnspan=2, pady=10)

    def show_account_choice(self):
        # Clear frames
        if hasattr(self, 'login_frame'):
            self.login_frame.pack_forget()
        if hasattr(self, 'create_account_frame'):
            self.create_account_frame.pack_forget()
        if hasattr(self, 'main_frame'):
            self.main_frame.pack_forget()

        self.account_frame.pack(pady=20)

    def login(self):
        account_name = self.account_name_entry.get()
        master_password = self.master_password_entry.get()

        if not account_name or not master_password:
            messagebox.showerror("Error", "Enter account name and password!")
            return

        self.password_manager = PasswordManager(account_name, master_password)
        if not self.password_manager.load_passwords():
            messagebox.showerror("Error", "Account does not exist or incorrect password!")
            return

        self.login_frame.pack_forget()
        self.show_main_menu()

    def create_account(self):
        account_name = self.new_account_name_entry.get()
        master_password = self.new_master_password_entry.get()

        if not account_name or not master_password:
            messagebox.showerror("Error", "Enter account name and password!")
            return

        if os.path.exists(f"passwords_{account_name}.enc"):
            messagebox.showerror("Error", "Account already exists!")
            return

        self.password_manager = PasswordManager(account_name, master_password)
        self.password_manager.save_passwords()

        messagebox.showinfo("Success", "Account created successfully!")
        self.create_account_frame.pack_forget()
        self.show_account_choice()

    def show_main_menu(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20)

        tk.Button(self.main_frame, text="Generate and Save Password", command=self.generate_and_save_password).pack(pady=5)
        tk.Button(self.main_frame, text="Show Passwords", command=self.show_passwords).pack(pady=5)
        tk.Button(self.main_frame, text="Export Passwords", command=self.export_passwords).pack(pady=5)
        tk.Button(self.main_frame, text="Import Passwords", command=self.import_passwords).pack(pady=5)
        tk.Button(self.main_frame, text="Logout", command=self.logout).pack(pady=5)

    def generate_and_save_password(self):
        platform = simpledialog.askstring("Platform", "Enter platform name (e.g., Gmail):")
        if not platform:
            return
        length = simpledialog.askinteger("Password Length", "Enter password length:", minvalue=8, maxvalue=50)
        if not length:
            return
        use_symbols = messagebox.askyesno("Symbols", "Include symbols?")
        use_digits = messagebox.askyesno("Digits", "Include digits?")
        use_uppercase = messagebox.askyesno("Uppercase", "Include uppercase letters?")

        password = generate_password(length, use_symbols, use_digits, use_uppercase)
        messagebox.showinfo("Generated Password", f"Your password: {password}")

        self.password_manager.add_password(platform, password)
        messagebox.showinfo("Success", f"Password for {platform} saved!")

    def show_passwords(self):
        passwords = self.password_manager.passwords
        if not passwords:
            messagebox.showinfo("No Passwords", "No passwords saved.")
        else:
            dialog = tk.Toplevel(self.root)
            dialog.title("Saved Passwords")
            dialog.geometry("400x300")

            text_widget = tk.Text(dialog, wrap=tk.WORD)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            for name, password in passwords.items():
                text_widget.insert(tk.END, f"{name}: {password}\n")
            text_widget.config(state=tk.DISABLED)

            tk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=5)

    def export_passwords(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            export_password = simpledialog.askstring("Password", "Enter password to encrypt the file:", show="*")
            if export_password:
                self.password_manager.export_to_json(filename, export_password)
                messagebox.showinfo("Success", "Passwords exported and encrypted!")
            else:
                messagebox.showerror("Error", "You must enter a password to encrypt!")

    def import_passwords(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            import_password = simpledialog.askstring("Password", "Enter password to decrypt the file:", show="*")
            if import_password:
                try:
                    self.password_manager.import_from_json(filename, import_password)
                    messagebox.showinfo("Success", "Passwords imported successfully!")
                except ValueError:
                    messagebox.showerror("Error", "Incorrect password file.")
            else:
                messagebox.showerror("Error", "You must enter a password to decrypt the file!")

    def logout(self):
        self.main_frame.pack_forget()
        self.account_frame.pack(pady=20)
        self.password_manager = None
