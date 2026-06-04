import json
from pathlib import Path
from datetime import datetime


class DeckRepository:

    def __init__(self, username, deck_name):
        self.deck_folder = Path("users") / username / deck_name
        self.deck_folder.mkdir(parents=True, exist_ok=True)

        self.game_config_file = self.deck_folder / "game_config.jsonl"
        self.preferences_file = self.deck_folder / "preferences.jsonl"
        self.questions_file = self.deck_folder / "questions.jsonl"
        self.ratings_file = self.deck_folder / "ratings.jsonl"

    # ===== WRITE =====

    def append_game_config(self, game_mode):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "game_mode": game_mode.value
        }

        self._append_jsonl(self.game_config_file, entry)

    def append_preferences(self, interests):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "interests": interests
        }

        self._append_jsonl(self.preferences_file, entry)

    def append_question(self, question):
        question_id = self._get_next_question_id()

        entry = {
            "id": question_id,
            "timestamp": datetime.now().isoformat(),
            "text": question
        }

        self._append_jsonl(self.questions_file, entry)

        return question_id

    def append_rating(self, question_id, rating):
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5.")

        entry = {
            "timestamp": datetime.now().isoformat(),
            "question_id": question_id,
            "rating": rating
        }

        self._append_jsonl(self.ratings_file, entry)

    def _append_jsonl(self, file_path, entry):
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def _get_next_question_id(self):
        if not self.questions_file.exists():
            return 1

        last_id = 0

        with open(self.questions_file, "r", encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    question = json.loads(line)
                    last_id = question["id"]

        return last_id + 1


    # ===== READ =====

    def read_game_config(self):
        return self._read_jsonl(self.game_config_file)

    def read_preferences(self):
        return self._read_jsonl(self.preferences_file)

    def read_questions(self):
        return self._read_jsonl(self.questions_file)

    def read_ratings(self):
        return self._read_jsonl(self.ratings_file)

    def read_latest_game_config(self):
        entries = self.read_game_config()
        return entries[-1] if entries else None

    def read_latest_preferences(self):
        entries = self.read_preferences()
        return entries[-1] if entries else None

    def _read_jsonl(self, file_path):
        if not file_path.exists():
            return []

        entries = []

        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    entries.append(json.loads(line))

        return entries