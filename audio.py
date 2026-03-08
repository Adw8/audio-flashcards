from pydub import AudioSegment

from config import Card, Config
from tts import speak


def silence(seconds: float) -> AudioSegment:
    return AudioSegment.silent(duration=int(seconds * 1000))


def build_card_audio(card: Card, cfg: Config, cache_dir: str = "./cache") -> AudioSegment:
    word_text = card.word
    if card.part_of_speech:
        word_segment = speak(word_text, cfg.voice, cache_dir) + silence(0.5) + speak(card.part_of_speech, cfg.voice, cache_dir)
    else:
        word_segment = speak(word_text, cfg.voice, cache_dir)

    track = word_segment * cfg.word_repeat
    track += silence(cfg.word_pause)
    track += speak(card.definition, cfg.voice, cache_dir)
    track += silence(cfg.definition_pause)

    if card.example and cfg.mode == "learn":
        track += speak(card.example, cfg.voice, cache_dir)
        track += silence(cfg.example_pause)

    track += silence(cfg.between_cards)
    return track


def export(audio: AudioSegment, path: str) -> None:
    audio.export(path, format="mp3")
