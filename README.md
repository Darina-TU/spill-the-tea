users/darina/
├── game_config.jsonl      # one entry when deck starts
├── preferences.jsonl      # one entry when deck starts, or when interests change
├── questions.jsonl        # grows every generated question
└── ratings.jsonl          # grows every rating

During initialization append once to:
game_config.jsonl
preferences.jsonl

During gameplay only append to:
questions.jsonl
ratings.jsonl




ui/
├── app.py
├── start_screen.py
├── deck_screen.py
├── setup_screen.py
└── game_screen.py

App
- owns the main Tkinter window
- switches between screens
- stores selected username/deck

StartScreen
- asks for username
- checks if user exists
- moves to DeckScreen

DeckScreen
- shows existing decks
- lets user choose existing deck
- or create a new deck

SetupScreen
- only for new decks
- asks game mode and interests
- saves game_config + preferences

GameScreen
- generates questions
- displays one unrated question at a time
- lets user rate 1–5
- shows NEXT / QUIT

Button click: "Start Game"
↓
DeckRepository(username, deck_name)
↓
PromptService(deck_repository)
↓
GameScreen displays questions