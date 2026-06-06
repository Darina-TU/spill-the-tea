# Spill the Tea Prototype

This is a local Python prototype of the party game **Spill the Tea**.  
It was built for an evaluation test and runs as a terminal application.

## How to start
Download the source code in your code editor of choice.
Add a .env file in the root directory with this line:
OPENAI_API_KEY=insert_your_chatgpt_api_key_here

Run the python script **terminal_app.py**.
Follow the instructions and start playing. 

## Goal
The app generates personalized party game questions based on:
- selected game mode
- user interests
- previously generated questions
- user ratings from 1 to 5

The prototype stores all data locally using JSON Lines files.

## University Evaluation
For our university project the prompts generated throughout the content experiment can be found under /users.
The participants have consented for their prompts to be made public on this GitHub repository.

## Project Structure

```text
spill-the-tea/
│── .env
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