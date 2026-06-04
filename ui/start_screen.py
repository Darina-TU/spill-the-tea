import tkinter as tk
from tkinter import messagebox


class StartScreen(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        tk.Label(self, text="Spill the Tea", font=("Arial", 28)).pack(pady=40)

        tk.Label(self, text="Username").pack()
        self.username_entry = tk.Entry(self, width=30)
        self.username_entry.pack(pady=10)

        tk.Button(
            self,
            text="Continue",
            command=self.continue_clicked
        ).pack(pady=20)

    def continue_clicked(self):
        username = self.username_entry.get().strip()

        if not username:
            messagebox.showerror("Error", "Please enter a username.")
            return

        self.app.show_deck_screen(username)