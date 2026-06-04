import tkinter as tk
from tkinter import messagebox

from configs import config


class SetupScreen(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        tk.Label(self, text="Create New Deck", font=("Arial", 22)).pack(pady=20)

        tk.Label(self, text="Choose game mode").pack()

        self.game_mode_var = tk.StringVar(value="1")

        tk.Radiobutton(
            self,
            text="Never Have I Ever",
            variable=self.game_mode_var,
            value="1"
        ).pack()

        tk.Radiobutton(
            self,
            text="Truth or Dare",
            variable=self.game_mode_var,
            value="2"
        ).pack()

        tk.Radiobutton(
            self,
            text="Mixed",
            variable=self.game_mode_var,
            value="3"
        ).pack()

        tk.Label(self, text="Interests, separated by commas").pack(pady=(30, 0))

        self.interests_entry = tk.Entry(self, width=60)
        self.interests_entry.pack(pady=10)

        tk.Button(
            self,
            text="Start Game",
            command=self.start_game
        ).pack(pady=20)

    def start_game(self):
        game_mode = self.get_selected_game_mode()
        interests = self.get_interests()

        if not interests:
            messagebox.showerror("Error", "Please enter at least one interest.")
            return

        self.app.deck_repository.append_game_config(game_mode)
        self.app.deck_repository.append_preferences(interests)

        self.app.show_game_screen()

    def get_selected_game_mode(self):
        choice = self.game_mode_var.get()

        if choice == "1":
            return config.GameMode.NEVER_HAVE_I_EVER
        if choice == "2":
            return config.GameMode.TRUTH_OR_DARE
        return config.GameMode.MIXED

    def get_interests(self):
        raw_text = self.interests_entry.get()

        interests = [
            interest.strip()
            for interest in raw_text.split(",")
            if interest.strip()
        ]

        return interests[:config.MAX_INTERESTS]