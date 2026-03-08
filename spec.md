# Audio Vocabulary Flashcard Generator

## Goal

Build a tool that converts a spreadsheet of vocabulary words into **audio flashcards** that can be played on a phone during activities like gym workouts.

The output should be **audio tracks with configurable pauses** so the listener has time to think before hearing the answer.

Primary constraint: **hands-free learning through continuous audio playback.**

---

# Core Use Case

User has a spreadsheet like:

| word | definition | part_of_speech | example |
|------|------------|----------------|---------|
| aberrant | markedly different from an accepted norm | adjective | When the financial director started screaming... |

The tool should:

1. Read the spreadsheet
2. Convert each row into spoken audio
3. Insert configurable pauses
4. Export playable audio files

---

# User Workflow

## 1. Prepare Spreadsheet

Supported formats:
- CSV
- XLSX (optional future feature)

Required columns:

```
word
definition
```

Optional columns:

```
part_of_speech
example
```

---

## 2. Run Generator

Example CLI command:

```
vocab-audio generate words.csv
```

Optional parameters:

```
--word-pause 3
--definition-pause 2
--example-pause 2
--between-cards 4
--word-repeat 2
--shuffle
--limit 10
--output-dir ./my-deck
--voice Samantha
--mode test
```

---

## 3. Output

Output directory:

```
output/
  001_aberrant.mp3
  002_capricious.mp3
  003_laconic.mp3
```

Tracks can be imported into any phone audio app.

Recommended players:
- Apple Music
- VLC
- Podcast apps

---

# Audio Structure

## Default Learning Mode

Playback structure for each card:

```
Word: Aberrant (adjective)       ← part_of_speech spoken if present
Word: Aberrant (adjective)       ← repeated word_repeat times total
[pause: word_pause]

Meaning: Markedly different from an accepted norm
[pause: definition_pause]

Example: When the financial director...
[pause: between_cards]
```

---

## Test Mode

Designed for recall practice. The word is repeated to give the listener time to recall the definition before it is spoken.

```
Word: Aberrant (adjective)       ← part_of_speech spoken if present
Word: Aberrant (adjective)       ← repeated word_repeat times total
[pause: word_pause]

Meaning: Markedly different from an accepted norm
[pause: between_cards]
```

---

## Reverse Mode (future)

```
Meaning: Markedly different from an accepted norm
[pause]

Word: Aberrant
```

---

# Configuration

Default values:

```
word_pause       = 3 seconds
definition_pause = 2 seconds
example_pause    = 2 seconds
between_cards    = 4 seconds
word_repeat      = 1
output_dir       = ./output
voice            = (system default)
limit            = (none, process all cards)
```

- `word_repeat` — how many times the word is spoken before the pause; `2` or `3` helps reinforce pronunciation and gives extra thinking time
- `output_dir` — where generated MP3s are written; created automatically if it doesn't exist
- `voice` — macOS voice name (e.g. `Samantha`, `Daniel`, `Karen`); defaults to the system TTS voice
- `limit` — process only the first N cards; useful for previewing output before a full run

Users can override all values via CLI flags.

---

# Technical Architecture

## Language

Python

Reasons:
- strong CSV support
- simple audio libraries
- easy CLI tools

---

## Dependencies

```
pydub
pandas
```

Optional:

```
ffmpeg
```

---

# Text-to-Speech Options

## Option 1 (recommended)

macOS built-in TTS

```bash
say -v Samantha -o output.aiff "text"
```

Advantages:
- free
- unlimited
- zero API setup
- multiple built-in voices selectable via `--voice`

---

## Option 2

pyttsx3 (offline Python TTS)

```python
import pyttsx3
engine = pyttsx3.init()
engine.save_to_file("Aberrant means markedly different from the norm", "aberrant.mp3")
engine.runAndWait()
```

---

## Option 3 (future upgrade)

Neural TTS systems for better voice quality.

---

# Audio Generation Pipeline

```
Spreadsheet
     ↓
Parse rows  (optionally shuffled, optionally limited to N)
     ↓
For each card → print "[3/50] capricious"
     ↓
Generate speech segments  (word × repeat, part_of_speech, definition, example)
     ↓
Insert silence segments
     ↓
Concatenate audio
     ↓
Export MP3 to output_dir
```

---

# Data Model

Internal representation:

```python
class Card:
    word: str
    definition: str
    part_of_speech: str | None
    example: str | None
```

---

# Audio Assembly

Example flow:

```
(word_audio + part_of_speech_audio) × word_repeat   ← part_of_speech_audio omitted if not present
+ silence(word_pause)
+ definition_audio
+ silence(definition_pause)
+ example_audio                                      ← omitted if not present
+ silence(between_cards)
```

---

# File Naming

Format:

```
{index}_{word}.mp3
```

Example:

```
001_aberrant.mp3
002_laconic.mp3
```

This keeps tracks ordered when imported to music apps.

---

# Optional Features (v2)

## Deck Generation

Generate one continuous file:

```
deck.mp3
```

Useful for uninterrupted listening sessions.

## Difficulty Levels

Allow reduced pauses for faster recall training.

```
--difficulty hard
```

Which might set:

```
word_pause       = 1
definition_pause = 1
```

---

# Performance Considerations

## TTS Caching

Avoid regenerating audio for identical text.

Strategy:

```
hash(text) -> filename
```

Store generated speech in a cache directory.

---

# Project Structure

```
project/
  generate.py   ← CLI entry point
  parser.py     ← read spreadsheet
  tts.py        ← generate speech
  audio.py      ← add pauses + merge tracks
  config.py     ← defaults and CLI arg parsing
  cache/
  output/
```

---

# MVP Scope

The first working version should support:

- CSV input
- `word` + `definition` fields
- optional `part_of_speech` spoken inline with the word
- configurable pauses
- configurable word repetition
- shuffle (`--shuffle`)
- voice selection (`--voice`)
- preview run (`--limit N`)
- configurable output directory (`--output-dir`)
- progress output printed per card during generation
- MP3 output
- individual tracks per card

Estimated implementation size: ~150–250 lines of Python

---

# Non-Goals (for now)

Do NOT build yet:

- mobile apps
- accounts
- databases
- web UI
- spaced repetition
- cloud infrastructure

Focus on audio generation only.

---

# Success Criteria

The tool is successful if:

- A user can generate audio from a spreadsheet in one command
- The output plays smoothly on a phone
- Pauses allow thinking time
- Listening works hands-free during workouts
