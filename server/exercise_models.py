from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class WordMultipleChoiceExercise:
    word: str
    meaning: str
    options: list[str]
    correct_option: str
