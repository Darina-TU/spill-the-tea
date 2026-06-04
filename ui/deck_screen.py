import tkinter as tk
from tkinter import messagebox
from pathlib import Path

class DeckScreen(tk.Frame):

    def __init__(self, parent, app, username):
        super().__init__(parent)
        self.app = app
        self.username = username

        tk.Label(self, text=f"User: {username}", font=("Arial", 20)).pack(pady=20)

        self.deck_listbox = tk.Listbox(self, width=40)
        self.deck_listbox.pack(pady=10)

        self.load_decks()
        self.deck_listbox.bind("<Double-Button-1>", self.play_selected_deck)

        tk.Button(
            self,
            text="Play selected deck",
            command=self.play_selected_deck
        ).pack(pady=10)

        tk.Label(self, text="New deck name").pack(pady=(30, 0))
        self.new_deck_entry = tk.Entry(self, width=30)
        self.new_deck_entry.pack(pady=10)

        tk.Button(
            self,
            text="Create new deck",
            command=self.create_new_deck
        ).pack(pady=10)

    def load_decks(self):
        user_folder = Path(__file__).parent.parent / "users" / self.username

        if not user_folder.exists():
            return

        decks = [
            folder.name
            for folder in user_folder.iterdir()
            if folder.is_dir()
        ]

        for deck in decks:
            self.deck_listbox.insert(tk.END, deck)

    def play_selected_deck(self, event=None):
        selection = self.deck_listbox.curselection()

        if not selection:
            messagebox.showerror("Error", "Please select a deck.")
            return

        deck_name = self.deck_listbox.get(selection[0])
        self.app.continue_existing_deck(deck_name)

    def create_new_deck(self):
        deck_name = self.new_deck_entry.get().strip()

        if not deck_name:
            messagebox.showerror("Error", "Please enter a deck name.")
            return

        self.app.show_setup_screen(deck_name)