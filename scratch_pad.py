from services.prompt_service import PromptService
from configs import config

prompt_service = PromptService("darina")

prompt = prompt_service.initial_prompt(
    game_mode=config.GameMode.TRUTH_OR_DARE.value,
    interests=["music", "travel", "funny stories"]
)

print(prompt)