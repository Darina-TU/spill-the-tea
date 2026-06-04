from repositories.deck_repository import DeckRepository
from services.prompt_service import PromptService

deck_repository = DeckRepository("darina", "deck2")
prompt_service = PromptService(deck_repository)

prompt = prompt_service.generate_prompt()

print(prompt)