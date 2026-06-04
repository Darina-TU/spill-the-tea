import json
import tkinter as tk
from tkinter import messagebox

from configs import config


class GameScreen(tk.Frame):

    def __init__(self, parent, app, client, deck_repository, prompt_service):
        super().__init__(parent)

        self.app = app
        self.client = client
        self.deck_repository = deck_repository
        self.prompt_service = prompt_service

        self.current_question = None

        tk.Label(self, text="Game", font=("Arial", 22)).pack(pady=20)

        self.question_label = tk.Label(
            self,
            text="",
            wraplength=650,
            font=("Arial", 16)
        )
        self.question_label.pack(pady=40)

        self.rating_var = tk.IntVar(value=3)

        self.rating_frame = tk.Frame(self)
        self.rating_frame.pack(pady=10)

        for rating in range(1, 6):
            tk.Radiobutton(
                self.rating_frame,
                text=str(rating),
                variable=self.rating_var,
                value=rating
            ).pack(side="left", padx=10)

        self.submit_button = tk.Button(
            self,
            text="Submit Rating",
            command=self.submit_rating
        )

        self.submit_button.pack(pady=20)

        self.next_round_button = tk.Button(
            self,
            text="Generate Next Round",
            command=self.generate_next_round
        )

        tk.Button(
            self,
            text="Quit",
            command=self.app.destroy
        ).pack(pady=10)

        self.load_or_generate_question()

    def load_or_generate_question(self):
        unrated_questions = self.get_unrated_questions()

        if not unrated_questions:
            self.current_question = None

            self.question_label.config(
                text="Round finished. Generate the next round?"
            )

            self.rating_frame.pack_forget()
            self.submit_button.pack_forget()

            self.next_round_button.pack(pady=10)

            return

        self.next_round_button.pack_forget()

        self.rating_frame.pack(pady=10)
        self.submit_button.pack(pady=20)

        self.next_round_button.pack_forget()
        self.current_question = unrated_questions[0]
        self.question_label.config(text=self.current_question["text"])

    def submit_rating(self):
        if not self.current_question:
            return

        rating = self.rating_var.get()

        self.deck_repository.append_rating(
            self.current_question["id"],
            rating
        )

        self.load_or_generate_question()

    def generate_next_round(self):
        self.next_round_button.pack_forget()
        self.generate_questions()
        self.load_or_generate_question()

    def generate_questions(self):
        prompt = self.prompt_service.generate_prompt()

        response = self.client.responses.create(
            model=config.MODEL_NAME,
            input=prompt
        )

        questions = self.parse_questions(response.output_text)

        for question in questions:
            self.deck_repository.append_question(question["text"])

    def parse_questions(self, response_text):
        cleaned = response_text.strip()

        if cleaned.startswith("```json"):
            cleaned = cleaned.replace("```json", "").replace("```", "").strip()
        elif cleaned.startswith("```"):
            cleaned = cleaned.replace("```", "").strip()

        data = json.loads(cleaned)

        return data["rated_questions"]

    def get_unrated_questions(self):
        questions = self.deck_repository.read_questions()
        ratings = self.deck_repository.read_ratings()

        rated_question_ids = {
            rating["question_id"]
            for rating in ratings
        }

        return [
            question for question in questions
            if question["id"] not in rated_question_ids
        ]