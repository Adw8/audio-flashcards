# audio-flashcards

CLI tool that converts a CSV file into spoken MP3 flashcard files using [Piper](https://github.com/rhasspy/piper) neural TTS.

## Requirements

- Python 3.10+
- `ffmpeg` (for MP3 export): `brew install ffmpeg`

```bash
brew install ffmpeg
pip install -r requirements.txt
```

## Usage

```
python generate.py input.csv [options]
```

### Options

| Flag | Default | Description |
|---|---|---|
| `--word-pause` | `3.0` | Silence after word (seconds) |
| `--definition-pause` | `2.0` | Silence after definition |
| `--example-pause` | `2.0` | Silence after example |
| `--between-cards` | `4.0` | Silence between cards |
| `--word-repeat` | `1` | Times to repeat the word |
| `--output-dir` | `./output` | Output directory |
| `--voice` | system default | Piper voice name (e.g. `en_US-lessac-medium`); run `--list-voices` to see all |
| `--mode` | `learn` | `learn` includes examples, `test` omits them |
| `--shuffle` | off | Randomise card order |
| `--limit N` | all | Process only first N cards |
| `--cards-per-deck N` | off | Split into decks of N cards each (output goes to `deck_1/`, `deck_2/`, …) |

### Examples

```bash
# Basic usage
python generate.py input.csv

# Quiz mode, shuffled, 10 cards, specific voice
python generate.py input.csv --mode test --shuffle --limit 10 --voice en_US-amy-medium

# Repeat each word 3 times with longer pauses
python generate.py input.csv --word-repeat 3 --word-pause 4 --definition-pause 3

# Split into decks of 20 cards
python generate.py input.csv --cards-per-deck 20
```

## Voices

TTS is powered by [Piper](https://github.com/rhasspy/piper). Voice models (~75 MB each)
are downloaded automatically on first use to `./voices/`.

Run `python generate.py --list-voices` to see all available voices:

```
Voice                                      Language         Gender   Quality
------------------------------------------------------------------------------
en_US-lessac-medium                        English (US)     Male     medium *
en_US-amy-medium                           English (US)     Female   medium
...
```

\* = default  |  voice files auto-download to `./voices/` on first use

Use a specific voice:
```bash
python generate.py input.csv --voice "en_US-amy-medium"
```

## Output

Each card is exported as a numbered MP3 in `./output/`:

```
output/
  001_ephemeral.mp3
  002_ubiquitous.mp3
  ...
```

When `--cards-per-deck` is used, cards are grouped into subdirectories:

```
output/
  deck_1/
    001_ephemeral.mp3
    ...
  deck_2/
    ...
```

Audio structure per card (learn mode):
```
[word] × word_repeat → pause → [definition] → pause → [example] → pause → [between-cards silence]
```

TTS audio is cached in `./cache/` by content hash so re-runs skip unchanged text.

---

## Current implementation: vocabulary flashcards

The tool is currently built around a word/definition flashcard format. The expected CSV schema is:

```csv
word,definition,part_of_speech,example
ephemeral,lasting for a very short time,adjective,The ephemeral beauty of cherry blossoms makes them all the more precious.
ubiquitous,present everywhere at the same time,adjective,Smartphones have become ubiquitous in modern life.
serendipity,the occurrence of happy events by chance,noun,
persevere,continue despite difficulty,,
```

- `word` and `definition` are required; rows missing either are skipped.
- `part_of_speech` and `example` are optional.
- In `learn` mode, the example sentence is read aloud; in `test` mode it is omitted.
