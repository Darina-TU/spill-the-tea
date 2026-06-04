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