from enum import Enum

# ===== OpenAI =====

MODEL_NAME = "gpt-5.4-mini"

# ===== Game Settings =====

QUESTIONS_PER_ROUND = 10

# ===== User Input =====

MAX_INTEREST_LENGTH = 16
MIN_INTEREST_LENGTH = 1
MAX_INTERESTS = 10

# ===== Game Modes =====

class GameMode(Enum):
    NEVER_HAVE_I_EVER = "Never Have I Ever"
    TRUTH_OR_DARE = "Truth or Dare"
    MIXED = "Mixed"

class QuestionType(Enum):
    TRUTH = "Truth"
    DARE = "Dare"
    NEVER_HAVE_I_EVER = "Never Have I Ever"

# ===== Ratings =====

class Rating(Enum):
    VERY_UNSATISFIED = 1
    UNSATISFIED = 2
    NOT_SURE = 3
    SATISFIED = 4
    VERY_SATISFIED = 5