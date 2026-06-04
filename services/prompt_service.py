import json
from pathlib import Path


class PromptService:

    def __init__(self, deck_repository):
        self.deck_repository = deck_repository

        self.base_prompt_file = Path("repositories") / "prompts" / "base_prompt.xml"
        self.prompt_folder = (
            Path("users")
            / deck_repository.username
            / "prompts"
        )
        self.prompt_folder.mkdir(parents=True, exist_ok=True)

    def generate_prompt(self):
        game_config = self.deck_repository.read_latest_game_config()
        preferences = self.deck_repository.read_latest_preferences()
        questions = self.deck_repository.read_questions()
        ratings = self.deck_repository.read_ratings()

        game_mode = game_config["game_mode"] if game_config else ""
        interests = preferences["interests"] if preferences else []

        input_data = {
            "interests": interests,
            "rated_questions": self._combine_questions_and_ratings(questions, ratings)
        }

        base_prompt = self._read_base_prompt()

        prompt = base_prompt.replace("{{GAME_MODE}}", game_mode)
        prompt = prompt.replace(
            "{{INPUT_DATA}}",
            json.dumps(input_data, ensure_ascii=False, indent=8)
        )

        self._save_prompt(prompt)

        return prompt

    def _read_base_prompt(self):
        with open(self.base_prompt_file, "r", encoding="utf-8") as file:
            return file.read()

    def _combine_questions_and_ratings(self, questions, ratings):
        rating_by_question_id = {
            rating["question_id"]: rating["rating"]
            for rating in ratings
        }

        rated_questions = []

        for question in questions:
            rated_questions.append({
                "id": question["id"],
                "text": question["text"],
                "rating": rating_by_question_id.get(question["id"])
            })

        return rated_questions

    def _save_prompt(self, prompt):
        prompt_id = self._get_next_prompt_id()
        prompt_file = self.prompt_folder / f"prompt_{prompt_id}.xml"

        with open(prompt_file, "w", encoding="utf-8") as file:
            file.write(prompt)

        return prompt_file

    def _get_next_prompt_id(self):
        existing_prompts = list(self.prompt_folder.glob("prompt_*.xml"))

        if not existing_prompts:
            return 1

        ids = [
            int(file.stem.replace("prompt_", ""))
            for file in existing_prompts
        ]

        return max(ids) + 1