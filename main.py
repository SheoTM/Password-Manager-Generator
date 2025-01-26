import tkinter as tk
from ui.app import PasswordManagerApp

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()
