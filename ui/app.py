import os
import tkinter as tk
from openai import OpenAI
from dotenv import load_dotenv

from repositories.deck_repository import DeckRepository
from services.prompt_service import PromptService
from ui.start_screen import StartScreen
from ui.deck_screen import DeckScreen
from ui.setup_screen import SetupScreen
from ui.game_screen import GameScreen


class App(tk.Tk):

    def __init__(self):
        super().__init__()

        load_dotenv()

        self.client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY")
        )

        self.title("Spill the Tea")
        self.geometry("800x600")

        self.username = None
        self.deck_name = None
        self.deck_repository = None
        self.prompt_service = None

        self.current_screen = None

        self.show_start_screen()

    def clear_screen(self):
        if self.current_screen:
            self.current_screen.destroy()

    def show_start_screen(self):
        self.clear_screen()
        self.current_screen = StartScreen(self, self)
        self.current_screen.pack(fill="both", expand=True)

    def show_deck_screen(self, username):
        self.username = username
        self.clear_screen()
        self.current_screen = DeckScreen(self, self, username)
        self.current_screen.pack(fill="both", expand=True)

    def show_setup_screen(self, deck_name):
        self.deck_name = deck_name
        self.deck_repository = DeckRepository(self.username, self.deck_name)
        self.prompt_service = PromptService(self.deck_repository)

        self.clear_screen()
        self.current_screen = SetupScreen(self, self)
        self.current_screen.pack(fill="both", expand=True)

    def continue_existing_deck(self, deck_name):
        self.deck_name = deck_name
        self.deck_repository = DeckRepository(self.username, self.deck_name)
        self.prompt_service = PromptService(self.deck_repository)

        self.show_game_screen()

    def show_game_screen(self):
        self.clear_screen()
        self.current_screen = GameScreen(
            self,
            self,
            self.client,
            self.deck_repository,
            self.prompt_service
        )
        self.current_screen.pack(fill="both", expand=True)