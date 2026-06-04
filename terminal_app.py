import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

from configs import config
from repositories.deck_repository import DeckRepository
from services.prompt_service import PromptService


def choose_game_mode():
    print("\nChoose game mode:")
    print("1 - Never Have I Ever")
    print("2 - Truth or Dare")
    print("3 - Mixed")

    choice = input("Your choice: ").strip()

    if choice == "1":
        return config.GameMode.NEVER_HAVE_I_EVER
    if choice == "2":
        return config.GameMode.TRUTH_OR_DARE
    if choice == "3":
        return config.GameMode.MIXED

    print("Invalid choice. Defaulting to Never Have I Ever.")
    return config.GameMode.NEVER_HAVE_I_EVER


def ask_interests():
    interests = []

    print("\nEnter interests. Press ENTER without typing to finish.")

    while len(interests) < config.MAX_INTERESTS:
        interest = input(f"Interest {len(interests) + 1}: ").strip()

        if interest == "":
            break

        if len(interest) > config.MAX_INTEREST_LENGTH:
            print(f"Too long. Max length is {config.MAX_INTEREST_LENGTH} characters.")
            continue

        interests.append(interest)

    return interests


def parse_questions(response_text):
    cleaned = response_text.strip()

    if cleaned.startswith("```json"):
        cleaned = cleaned.replace("```json", "").replace("```", "").strip()
    elif cleaned.startswith("```"):
        cleaned = cleaned.replace("```", "").strip()

    data = json.loads(cleaned)

    return data["rated_questions"]


def generate_questions(client, prompt_service, deck_repository):
    prompt = prompt_service.generate_prompt()

    response = client.responses.create(
        model=config.MODEL_NAME,
        input=prompt
    )

    questions = parse_questions(response.output_text)

    saved_question_ids = []

    for question in questions:
        question_id = deck_repository.append_question(question["text"])
        saved_question_ids.append(question_id)

    return saved_question_ids


def play_unrated_questions(deck_repository):
    questions = deck_repository.read_questions()
    ratings = deck_repository.read_ratings()

    rated_question_ids = {
        rating["question_id"]
        for rating in ratings
    }

    unrated_questions = [
        question for question in questions
        if question["id"] not in rated_question_ids
    ]

    for question in unrated_questions:
        print("\nQuestion:")
        print(question["text"])

        while True:
            rating_input = input("Rating 1-5: ").strip()

            try:
                rating = int(rating_input)
                deck_repository.append_rating(question["id"], rating)
                break
            except ValueError:
                print("Please enter a number from 1 to 5.")

def choose_username():
    return input("Username: ").strip()


def get_existing_decks(username):
    user_folder = Path("users") / username

    if not user_folder.exists():
        return []

    return [
        folder.name
        for folder in user_folder.iterdir()
        if folder.is_dir() and folder.name != "prompts"
    ]


def choose_or_create_deck(username):
    existing_decks = get_existing_decks(username)

    if not existing_decks:
        print("\nNo existing decks found.")
        return create_new_deck_name()

    print("\nExisting decks:")
    for index, deck in enumerate(existing_decks, start=1):
        print(f"{index} - {deck}")

    print("N - Create new deck")

    choice = input("Choose deck or create new one: ").strip()

    if choice.upper() == "N":
        return create_new_deck_name()

    try:
        deck_index = int(choice) - 1
        return existing_decks[deck_index]
    except (ValueError, IndexError):
        print("Invalid choice. Creating new deck.")
        return create_new_deck_name()


def create_new_deck_name():
    return input("New deck name: ").strip()

def main():
    load_dotenv()

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )

    username = choose_username()
    deck_name = choose_or_create_deck(username)

    deck_repository = DeckRepository(username, deck_name)
    prompt_service = PromptService(deck_repository)

    is_new_deck = not deck_repository.read_latest_game_config()

    if is_new_deck:
        game_mode = choose_game_mode()
        interests = ask_interests()

        deck_repository.append_game_config(game_mode)
        deck_repository.append_preferences(interests)
    else:
        print(f"\nContinuing existing deck: {deck_name}")

    while True:
        print("\nGenerating questions...")
        generate_questions(client, prompt_service, deck_repository)

        play_unrated_questions(deck_repository)

        while True:
            next_action = input(
                "\nType NEXT for another round or QUIT to stop: "
            ).strip().upper()

            if next_action == "NEXT":
                break

            if next_action == "QUIT":
                print("Game ended.")
                return

            print("Invalid input. Please enter NEXT or QUIT.")


if __name__ == "__main__":
    main()