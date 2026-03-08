import argparse
import os
import random

from audio import build_card_audio, export
from config import Config
from parser import parse_csv

CACHE_DIR = "./cache"


def main():
    parser = argparse.ArgumentParser(description="Generate audio flashcards from a CSV vocabulary file.")
    parser.add_argument("csv", help="Path to vocabulary CSV file")
    parser.add_argument("--word-pause", type=float, default=3.0)
    parser.add_argument("--definition-pause", type=float, default=2.0)
    parser.add_argument("--example-pause", type=float, default=2.0)
    parser.add_argument("--between-cards", type=float, default=4.0)
    parser.add_argument("--word-repeat", type=int, default=1)
    parser.add_argument("--shuffle", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--output-dir", default="./output")
    parser.add_argument("--voice", default=None)
    parser.add_argument("--mode", choices=["learn", "test"], default="learn")
    args = parser.parse_args()

    cfg = Config(
        word_pause=args.word_pause,
        definition_pause=args.definition_pause,
        example_pause=args.example_pause,
        between_cards=args.between_cards,
        word_repeat=args.word_repeat,
        output_dir=args.output_dir,
        voice=args.voice,
        limit=args.limit,
        shuffle=args.shuffle,
        mode=args.mode,
    )

    cards = parse_csv(args.csv)

    if cfg.shuffle:
        random.shuffle(cards)

    if cfg.limit is not None:
        cards = cards[:cfg.limit]

    os.makedirs(cfg.output_dir, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)

    total = len(cards)
    for i, card in enumerate(cards, start=1):
        print(f"[{i}/{total}] {card.word}")
        audio = build_card_audio(card, cfg, cache_dir=CACHE_DIR)
        filename = f"{i:03d}_{card.word.lower().replace(' ', '_')}.mp3"
        export(audio, os.path.join(cfg.output_dir, filename))


if __name__ == "__main__":
    main()
