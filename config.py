from dataclasses import dataclass, field


@dataclass
class Config:
    word_pause: float = 3.0
    definition_pause: float = 2.0
    example_pause: float = 2.0
    between_cards: float = 4.0
    word_repeat: int = 1
    output_dir: str = "./output"
    voice: str | None = None
    limit: int | None = None
    shuffle: bool = False
    mode: str = "learn"


@dataclass
class Card:
    word: str
    definition: str
    part_of_speech: str | None = None
    example: str | None = None
