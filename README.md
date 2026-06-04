# Spill the Tea Prototype

This is a local Python prototype of the party game **Spill the Tea**.  
It was built for an evaluation test and runs as a terminal application.

## Goal

The app generates personalized party game questions based on:

- selected game mode
- user interests
- previously generated questions
- user ratings from 1 to 5

The prototype stores all data locally using JSON Lines files.

## Project Structure

```text
spill-the-tea/
│
├── terminal_app.py
├── configs/
│   └── config.py
│
├── repositories/
│   ├── deck_repository.py
│   └── prompts/
│       └── base_prompt.xml
│
├── services/
│   └── prompt_service.py
│
└── users/
    └── username/
        └── deck_name/
            ├── game_config.jsonl
            ├── preferences.jsonl
            ├── questions.jsonl
            ├── ratings.jsonl
            └── prompts/
                └── prompt_1.xml