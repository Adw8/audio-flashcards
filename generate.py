import argparse
import json
import os
import random

from audio import build_card_audio, export
from config import Config
from parser import parse_csv

CACHE_DIR = "./cache"


def main():
    parser = argparse.ArgumentParser(description="Generate audio flashcards from a CSV vocabulary file.")
    parser.add_argument("csv", nargs="?", help="Path to vocabulary CSV file")
    parser.add_argument("--list-voices", action="store_true", help="List available Piper voices and exit")
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

    if args.list_voices:
        with open(os.path.join(os.path.dirname(__file__), "voices.json")) as f:
            voices = json.load(f)
        print(f"{'Voice':<42} {'Language':<16} {'Gender':<8} Quality")
        print("-" * 78)
        for v in voices:
            marker = " *" if v.get("default") else "  "
            print(f"{v['name']:<42} {v['lang']:<16} {v['gender']:<8} {v['quality']}{marker}")
        print("\n* = default  |  voice files auto-download to ./voices/ on first use")
        return
    if not args.csv:
        parser.error("csv is required unless --list-voices is used")

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
