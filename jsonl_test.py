from services.jsonl_service import JsonlService
from configs import config

user = "darina"
deck = "deck2"
interest1 = "hiking"
interest2 = "boxing"
question = "Never have I hit someone."

jsonl_service = JsonlService(user, deck)

# ===== WRITE =====
# jsonl_service.append_game_config(config.GameMode.MIXED) # once
# jsonl_service.append_preferences([interest1, interest2]) # once
#
# question_id = jsonl_service.append_question(question)
# jsonl_service.append_rating(question_id, 3)
# print("Saved test data.")

# ===== READ =====
game_config = jsonl_service.read_latest_game_config()
preferences = jsonl_service.read_latest_preferences()
questions = jsonl_service.read_questions()
ratings = jsonl_service.read_ratings()

print("Game config:")
print(game_config)

print("Preferences:")
print(preferences)

print("Questions:")
print(questions)

print("Ratings:")
print(ratings)