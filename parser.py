import csv
from config import Card


def parse_csv(path: str) -> list[Card]:
    cards = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            word = row.get("word", "").strip()
            definition = row.get("definition", "").strip()
            if not word or not definition:
                continue
            part_of_speech = row.get("part_of_speech", "").strip() or None
            example = row.get("example", "").strip() or None
            cards.append(Card(word=word, definition=definition, part_of_speech=part_of_speech, example=example))
    return cards
