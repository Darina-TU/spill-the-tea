import json
from pathlib import Path
from datetime import datetime


class PromptService:

    def __init__(self, username):
        self.username = username
        self.user_folder = Path("users") / username
        self.prompt_log_file = self.user_folder / "prompt.jsonl"

        self.user_folder.mkdir(parents=True, exist_ok=True)

    def initial_prompt(self, game_mode, interests):
        base_prompt = self._read_base_prompt()

        prompt = base_prompt.replace("{{GAME_MODE}}", game_mode)
        prompt = prompt.replace("{{INTERESTS}}", json.dumps(interests))

        self._log_prompt(prompt, "initial")

        return prompt

    def _read_base_prompt(self):
        with open("repositories/prompts/base_prompt.xml", "r", encoding="utf-8") as file:
            return file.read()

    def _log_prompt(self, prompt, prompt_type):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": prompt_type,
            "prompt": prompt
        }

        with open(self.prompt_log_file, "a", encoding="utf-8") as file:
            file.write(json.dumps(log_entry, ensure_ascii=False) + "\n")