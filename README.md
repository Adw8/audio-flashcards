# audio-flashcards

CLI tool that converts a CSV vocabulary list into spoken MP3 flashcard files using macOS text-to-speech.

## Requirements

- Python 3.10+
- `ffmpeg` (for MP3 export): `brew install ffmpeg`

```bash
brew install ffmpeg
pip install -r requirements.txt
```

## CSV Format

```csv
word,definition,part_of_speech,example
ephemeral,lasting for a very short time,adjective,The ephemeral beauty of cherry blossoms makes them all the more precious.
```

`part_of_speech` and `example` columns are optional. Rows missing `word` or `definition` are skipped.

## Usage

```
python generate.py words.csv [options]
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
| `--voice` | system default | macOS voice name (e.g. `Samantha`, `Daniel`) |
| `--mode` | `learn` | `learn` includes examples, `test` omits them |
| `--shuffle` | off | Randomise card order |
| `--limit N` | all | Process only first N cards |

### Examples

```bash
# Basic usage
python generate.py words.csv

# Quiz mode, shuffled, 10 cards, specific voice
python generate.py words.csv --mode test --shuffle --limit 10 --voice Samantha

# Repeat each word 3 times with longer pauses
python generate.py words.csv --word-repeat 3 --word-pause 4 --definition-pause 3
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
python generate.py words.csv --voice "en_US-amy-medium"
```

## Output

Each card is exported as a numbered MP3 in `./output/`:

```
output/
  001_ephemeral.mp3
  002_ubiquitous.mp3
  ...
```

Audio structure per card (learn mode):
```
[word] × word_repeat → pause → [definition] → pause → [example] → pause → [between-cards silence]
```

TTS audio is cached in `./cache/` by content hash so re-runs skip unchanged text.
